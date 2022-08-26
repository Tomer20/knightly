# !/usr/bin/env python3.10
# -*- coding: utf-8 -*-
import conf
import logging
from kubernetes import client, config


logger_format = '[%(asctime)s]  [%(levelname)s]\t%(message)s'
logging.basicConfig(format=logger_format, datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger('DevOps')
logger.setLevel(conf.LOG_LEVEL)


class Annotator:

    def __init__(self) -> None:
        if conf.RUN_IN_CLUSTER == "True":
            config.load_incluster_config()
        else:
            config.load_kube_config(conf.SCRIPT_KUBECONFIG)
        self.k_client = client.CoreV1Api()

    def get_namespaces(self) -> list:
        logger.info("Getting knightly disabled namespaces")
        all_namespaces = self.k_client.list_namespace().items
        knightly_excluded_namespaces = self.k_client.list_namespace(
            label_selector=f"{conf.Namespace.LABEL} in (excluded,true)").items
        excluded_namespaces = [ns.metadata.name for ns
                               in knightly_excluded_namespaces]
        namespaces = [ns for ns in all_namespaces
                      if ns.metadata.name not in excluded_namespaces]
        logger.debug(f"All namespaces found: {all_namespaces}")
        logger.debug(f"Excluded namespaces: {excluded_namespaces}")
        logger.debug(f"Final list of namespaces: {namespaces}")
        return namespaces

    def annotate_namespace(self, namespace) -> None:
        ns_name = namespace.metadata.name
        logger.info(f"Working on namespace {ns_name}")
        try:
            days_to_keep = int(namespace.metadata.annotations.get(
                conf.Namespace.ANNOTATION, '0'))
        except AttributeError:  # When no annotation, we'll add it.
            days_to_keep = 0
        if days_to_keep > 1:
            enabled = "false"
            days_to_keep -= days_to_keep
            logger.info(f"Need to keep namespace {ns_name} up for "
                        f"{days_to_keep} more days")
        else:
            enabled = "true"
            days_to_keep = 0
            logger.info(f"Enabling knightly scaler on namespace {ns_name}")
        patch = {
            "metadata": {
                "labels": {
                    conf.Namespace.LABEL: enabled
                },
                "annotations": {
                    # Annotations must be strings. `None` value to delete them.
                    conf.Namespace.ANNOTATION: str(days_to_keep)
                }
            }
        }
        self.k_client.patch_namespace(name=ns_name, body=patch)
        logger.info(f"Patched {ns_name}")


def main() -> None:
    annotator = Annotator()
    for ns in annotator.get_namespaces():
        annotator.annotate_namespace(ns)


if __name__ == '__main__':
    main()
