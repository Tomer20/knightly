# !/usr/bin/env python3.10
# -*- coding: utf-8 -*-
from enum import Enum
import os

RUN_IN_CLUSTER = os.getenv("RUN_IN_CLUSTER", default="False")
if RUN_IN_CLUSTER == "False":
    SCRIPT_KUBECONFIG = os.getenv("SCRIPT_KUBECONFIG",
                                  default="~/.kube/config.everc_dev")
LOG_LEVEL = os.getenv("LOG_LEVEL", default="INFO")


class Namespace(str, Enum):
    LABEL = "knightly.everc.com/enabled"
    ANNOTATION = "knightly.everc.com/keepmeup"
