# !/usr/bin/env python3.10
# -*- coding: utf-8 -*-
from enum import Enum
import os

RUN_IN_CLUSTER = os.getenv("RUN_IN_CLUSTER", default="False")
if RUN_IN_CLUSTER == "False":
    SCRIPT_KUBECONFIG = os.getenv("SCRIPT_KUBECONFIG",
                                  default="~/.kube/config.everc_dev")
LOG_LEVEL = os.getenv("LOG_LEVEL", default="INFO")


class Keda(str, Enum):
    API_VERSION = "keda.sh/v1alpha1"
    KIND = "ScaledObject"
    ANNOTATION = "autoscaling.keda.sh/paused-replicas"
    PATCH_CONTENT_TYPE = "application/merge-patch+json"


class Namespace(str, Enum):
    LABEL = "knightly.everc.com/enabled"
    ANNOTATION = "knightly.everc.com/keepmeup"
