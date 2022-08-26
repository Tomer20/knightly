# !/usr/bin/env python3.10
# -*- coding: utf-8 -*-
import conf
from logger import logger
from kubernetes import client, config, dynamic
from kubernetes.client import api_client


class KubeControls:

    def __init__(self) -> None:
        if conf.RUN_IN_CLUSTER == "True":
            config.load_incluster_config()
        else:
            config.load_kube_config(conf.SCRIPT_KUBECONFIG)
        self.k_core_client = client.CoreV1Api()
        self.k_apps_client = client.AppsV1Api()
        k_dynamic_client = dynamic.DynamicClient(api_client.ApiClient())
        self.scaled_object_api = k_dynamic_client.resources.get(
            api_version=conf.Keda.API_VERSION, kind=conf.Keda.KIND)

    def __handle_namespace(self, command, namespace, days_to_keep=0) -> None:
        logger.info(f"Handling namespace {namespace}")
        if command == conf.Commands.STOP or command == conf.Commands.START:
            enabled = "true"
        elif command == conf.Commands.KEEPMEUP:
            enabled = "false"
        patch = {
            "metadata": {
                "labels": {
                    conf.Namespace.LABEL: enabled
                },
                "annotations": {
                    conf.Namespace.ANNOTATION: str(days_to_keep)
                }
            }
        }
        self.k_core_client.patch_namespace(name=namespace, body=patch)
        logger.info(f"Patched namespace {namespace} "
                    f"with [{enabled},{days_to_keep}]")

    def __handle_scaled_objects(self, command, namespace) -> None:
        if command == conf.Commands.STOP:
            annotation_value = "0"
        elif command == conf.Commands.START:
            annotation_value = None    # `None` will remove the annotation
        scaledobjects = self.scaled_object_api.get(namespace=namespace).items
        logger.debug(f"{namespace} scaledobjects: {scaledobjects}")
        for scaledob in scaledobjects:
            scaledob_name = scaledob.metadata.name
            logger.info(
                f"{namespace}/{scaledob_name} patching pause annotation")
            setattr(scaledob.metadata.annotations,
                    conf.Keda.ANNOTATION, annotation_value)
            patch = {
                "metadata": {
                    "annotations": dict(scaledob.metadata.annotations)
                }
            }
            self.scaled_object_api.patch(
                body=patch, name=scaledob_name, namespace=namespace,
                content_type=conf.Keda.PATCH_CONTENT_TYPE)

    def __handle_deployments(self, command, namespace) -> None:
        if command == conf.Commands.STOP:
            replicas = 0
        elif command == conf.Commands.START:
            replicas = 1
        patch = {
            "spec": {
                "replicas": replicas
            }
        }
        deployments = self.k_apps_client.list_namespaced_deployment(
            namespace).items
        logger.debug(f"{namespace} deployments: {deployments}")
        for depl in deployments:
            depl_name = depl.metadata.name
            current_replicas = depl.spec.replicas
            logger.info(f"{namespace}/{depl_name} num of replicas: "
                        f"{current_replicas}. Patching to {replicas}")
            self.k_apps_client.patch_namespaced_deployment_scale(
                name=depl_name, namespace=namespace, body=patch)

    def __stop_start_namespace(self, command, namespace) -> None:
        logger.info(f"{command} namespace {namespace}")
        self.__handle_namespace(command, namespace, 0)
        self.__handle_scaled_objects(command, namespace)
        self.__handle_deployments(command, namespace)

    def __keep_namespace_up(self, namespace, days_to_keep) -> None:
        logger.info(f"Setting namespace {namespace} "
                    f"to stay up {days_to_keep} days")
        self.__handle_namespace(
            conf.Commands.KEEPMEUP, namespace, days_to_keep)

    def namespace_handler(self, command, resource_name, command_text) -> str:
        try:
            if command == conf.Commands.STOP:
                self.__stop_start_namespace(command, resource_name)
                msg = f"Namespace `{resource_name}` is stopping."
            elif command == conf.Commands.START:
                self.__stop_start_namespace(command, resource_name)
                msg = f"Namespace `{resource_name}` is starting."
            elif command == conf.Commands.KEEPMEUP:
                try:
                    days_to_keep = int(command_text[3])
                except ValueError:
                    msg = "Error: number of days to keep " \
                        f"(`{command_text[3]}`) must be an integer."
                    logger.error(msg)
                    return msg
                except IndexError:
                    msg = "Error: you must provide number of days to keep."
                    logger.error(msg)
                    return msg
                if days_to_keep > int(conf.Validations.MAX_DAYS_TO_KEEP):
                    msg = "Error: maximun number of days " \
                        f"to keep is {conf.Validations.MAX_DAYS_TO_KEEP}."
                    logger.error(msg)
                elif days_to_keep < 1:
                    msg = "Error: minimum number of days to keep is 1."
                    logger.error(msg)
                else:
                    self.__keep_namespace_up(resource_name, days_to_keep)
                    msg = f"Namespace `{resource_name}` will stay up " \
                        f"for {days_to_keep} days."
            return msg
        except Exception as e:
            if e.status == 404:
                msg = f"Error: namespace `{resource_name}` was not found."
            else:
                msg = f"Error: something else...\n{e}"
            logger.error(msg)
            return msg


k8s = KubeControls()
