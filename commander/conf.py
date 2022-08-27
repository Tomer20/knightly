# !/usr/bin/env python3.10
# -*- coding: utf-8 -*-
from enum import Enum
import os

RUN_IN_CLUSTER = os.getenv("RUN_IN_CLUSTER", default="False")
if RUN_IN_CLUSTER == "False":
    SCRIPT_KUBECONFIG = os.getenv("SCRIPT_KUBECONFIG",
                                  default="~/.kube/config")
LOG_LEVEL = os.getenv("LOG_LEVEL", default="INFO")
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 3000))
SLACK_COMMAND = os.getenv("SLACK_COMMAND", "knightly")
MAX_DAYS_TO_KEEP = int(os.getenv("MAX_DAYS_TO_KEEP", 7))


class Routes(str, Enum):
    HEALTH = "/healthz"
    COMMAND = f"/{SLACK_COMMAND}"


class Commands(str, Enum):
    START = "start"
    STOP = "stop"
    KEEPMEUP = "keep"


class Validations(str, Enum):
    MAX_DAYS_TO_KEEP = MAX_DAYS_TO_KEEP


class ResourceTypes(str, Enum):
    NAMESPACE = "namespace"
    DATABASE = "database"


class Keda(str, Enum):
    API_VERSION = "keda.sh/v1alpha1"
    KIND = "ScaledObject"
    ANNOTATION = "autoscaling.keda.sh/paused-replicas"
    PATCH_CONTENT_TYPE = "application/merge-patch+json"


class Namespace(str, Enum):
    LABEL = "knightly.example.com/enabled"
    ANNOTATION = "knightly.example.com/keepmeup"
