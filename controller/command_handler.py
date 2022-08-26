# !/usr/bin/env python3.10
# -*- coding: utf-8 -*-
from k8s import k8s
from logger import logger
import conf


async def command_handler(request_form) -> str:
    command_text = request_form["text"].split()
    command = command_text[0]
    resource_type = command_text[1]
    resource_name = command_text[2]
    logger.info(f"Handling the command `{command}`")
    try:
        if command not in conf.Commands._value2member_map_:
            msg = f"Error: `{command}` is not a valid command."
            logger.error(msg)
            return msg
        elif resource_type not in conf.ResourceTypes._value2member_map_:
            msg = f"Error: `{resource_type}` is not a valid resource type."
            logger.error(msg)
            return msg
        if resource_type == conf.ResourceTypes.NAMESPACE:
            msg = k8s.namespace_handler(command, resource_name, command_text)
        elif resource_type == conf.ResourceTypes.DATABASE:
            msg = "Error: databases aren't supported yet."
            logger.error(msg)
        return msg
    except Exception as e:
        logger.error(e)
        return e
