# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Union

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    unset,
    UnsetType,
)


class CloudWorkloadSecurityAgentRuleCreateAttributes(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "description": (str,),
            "enabled": (bool,),
            "expression": (str,),
            "name": (str,),
        }

    attribute_map = {
        "description": "description",
        "enabled": "enabled",
        "expression": "expression",
        "name": "name",
    }

    def __init__(
        self_,
        expression: str,
        name: str,
        description: Union[str, UnsetType] = unset,
        enabled: Union[bool, UnsetType] = unset,
        **kwargs,
    ):
        """
        Create a new Cloud Workload Security Agent rule.

        :param description: The description of the Agent rule.
        :type description: str, optional

        :param enabled: Whether the Agent rule is enabled.
        :type enabled: bool, optional

        :param expression: The SECL expression of the Agent rule.
        :type expression: str

        :param name: The name of the Agent rule.
        :type name: str
        """
        if description is not unset:
            kwargs["description"] = description
        if enabled is not unset:
            kwargs["enabled"] = enabled
        super().__init__(kwargs)

        self_.expression = expression
        self_.name = name
