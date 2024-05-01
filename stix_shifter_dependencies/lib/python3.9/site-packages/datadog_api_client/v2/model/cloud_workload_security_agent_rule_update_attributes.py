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


class CloudWorkloadSecurityAgentRuleUpdateAttributes(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "description": (str,),
            "enabled": (bool,),
            "expression": (str,),
        }

    attribute_map = {
        "description": "description",
        "enabled": "enabled",
        "expression": "expression",
    }

    def __init__(
        self_,
        description: Union[str, UnsetType] = unset,
        enabled: Union[bool, UnsetType] = unset,
        expression: Union[str, UnsetType] = unset,
        **kwargs,
    ):
        """
        Update an existing Cloud Workload Security Agent rule.

        :param description: The description of the Agent rule.
        :type description: str, optional

        :param enabled: Whether the Agent rule is enabled.
        :type enabled: bool, optional

        :param expression: The SECL expression of the Agent rule.
        :type expression: str, optional
        """
        if description is not unset:
            kwargs["description"] = description
        if enabled is not unset:
            kwargs["enabled"] = enabled
        if expression is not unset:
            kwargs["expression"] = expression
        super().__init__(kwargs)
