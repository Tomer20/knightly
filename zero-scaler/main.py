# !/usr/bin/env python3.10
# -*- coding: utf-8 -*-
import conf
import logging
from kubernetes import client, config, dynamic
from kubernetes.client import api_client


logger_format = '[%(asctime)s]  [%(levelname)s]\t%(message)s'
logging.basicConfig(format=logger_format, datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger('DevOps')
logger.setLevel(conf.LOG_LEVEL)


class ZeroScaler:

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

    def get_namespaces(self) -> list:
        namespaces = list()
        logger.info("Getting knightly enabled namespaces")
        namespaces = self.k_client.list_namespace(
            label_selector=f"{conf.Namespace.LABEL}=true")
        logger.debug(f"Namespaces found: {namespaces.items}")
        return namespaces.items

    def pause_scaled_objects(self, namespace) -> None:
        scaledobjects = self.scaled_object_api.get(namespace=namespace).items
        logger.debug(f"{namespace} scaledobjects: {scaledobjects}")
        for scaledob in scaledobjects:
            scaledob_name = scaledob.metadata.name
            logger.info(
                f"{namespace}/{scaledob_name} patching pause annotation")
            patch = {
                "metadata": {
                    "annotations": {
                        # Annotations must be strings.
                        conf.Keda.ANNOTATION: "0"
                    }
                }
            }
            self.scaled_object_api.patch(
                body=patch, name=scaledob_name, namespace=namespace,
                content_type=conf.Keda.PATCH_CONTENT_TYPE)

    def scale_deployments(self, namespace) -> None:
        deployments = self.k_apps_client.list_namespaced_deployment(
            namespace).items
        logger.debug(f"{namespace} deployments: {deployments}")
        patch = {
            "spec": {
                "replicas": 0
            }
        }
        for depl in deployments:
            depl_name = depl.metadata.name
            current_replicas = depl.spec.replicas
            if current_replicas != 0:
                logger.info(f"{namespace}/{depl_name} num of "
                            f"replicas: {current_replicas}")
                self.k_apps_client.patch_namespaced_deployment_scale(
                    name=depl_name, namespace=namespace, body=patch)


def main() -> None:
    zero_scaler = ZeroScaler()
    for ns in zero_scaler.get_namespaces():
        ns_name = ns.metadata.name
        zero_scaler.pause_scaled_objects(ns_name)
        zero_scaler.scale_deployments(ns_name)


if __name__ == '__main__':
    main()
