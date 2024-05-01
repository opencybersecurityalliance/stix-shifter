# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Union, TYPE_CHECKING

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    unset,
    UnsetType,
)


if TYPE_CHECKING:
    from datadog_api_client.v2.model.cloud_workload_security_agent_rule_creator_attributes import (
        CloudWorkloadSecurityAgentRuleCreatorAttributes,
    )
    from datadog_api_client.v2.model.cloud_workload_security_agent_rule_updater_attributes import (
        CloudWorkloadSecurityAgentRuleUpdaterAttributes,
    )


class CloudWorkloadSecurityAgentRuleAttributes(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.cloud_workload_security_agent_rule_creator_attributes import (
            CloudWorkloadSecurityAgentRuleCreatorAttributes,
        )
        from datadog_api_client.v2.model.cloud_workload_security_agent_rule_updater_attributes import (
            CloudWorkloadSecurityAgentRuleUpdaterAttributes,
        )

        return {
            "category": (str,),
            "creation_date": (int,),
            "creator": (CloudWorkloadSecurityAgentRuleCreatorAttributes,),
            "default_rule": (bool,),
            "description": (str,),
            "enabled": (bool,),
            "expression": (str,),
            "name": (str,),
            "updated_at": (int,),
            "updater": (CloudWorkloadSecurityAgentRuleUpdaterAttributes,),
            "version": (int,),
        }

    attribute_map = {
        "category": "category",
        "creation_date": "creationDate",
        "creator": "creator",
        "default_rule": "defaultRule",
        "description": "description",
        "enabled": "enabled",
        "expression": "expression",
        "name": "name",
        "updated_at": "updatedAt",
        "updater": "updater",
        "version": "version",
    }

    def __init__(
        self_,
        category: Union[str, UnsetType] = unset,
        creation_date: Union[int, UnsetType] = unset,
        creator: Union[CloudWorkloadSecurityAgentRuleCreatorAttributes, UnsetType] = unset,
        default_rule: Union[bool, UnsetType] = unset,
        description: Union[str, UnsetType] = unset,
        enabled: Union[bool, UnsetType] = unset,
        expression: Union[str, UnsetType] = unset,
        name: Union[str, UnsetType] = unset,
        updated_at: Union[int, UnsetType] = unset,
        updater: Union[CloudWorkloadSecurityAgentRuleUpdaterAttributes, UnsetType] = unset,
        version: Union[int, UnsetType] = unset,
        **kwargs,
    ):
        """
        A Cloud Workload Security Agent rule returned by the API.

        :param category: The category of the Agent rule.
        :type category: str, optional

        :param creation_date: When the Agent rule was created, timestamp in milliseconds.
        :type creation_date: int, optional

        :param creator: The attributes of the user who created the Agent rule.
        :type creator: CloudWorkloadSecurityAgentRuleCreatorAttributes, optional

        :param default_rule: Whether the rule is included by default.
        :type default_rule: bool, optional

        :param description: The description of the Agent rule.
        :type description: str, optional

        :param enabled: Whether the Agent rule is enabled.
        :type enabled: bool, optional

        :param expression: The SECL expression of the Agent rule.
        :type expression: str, optional

        :param name: The name of the Agent rule.
        :type name: str, optional

        :param updated_at: When the Agent rule was last updated, timestamp in milliseconds.
        :type updated_at: int, optional

        :param updater: The attributes of the user who last updated the Agent rule.
        :type updater: CloudWorkloadSecurityAgentRuleUpdaterAttributes, optional

        :param version: The version of the Agent rule.
        :type version: int, optional
        """
        if category is not unset:
            kwargs["category"] = category
        if creation_date is not unset:
            kwargs["creation_date"] = creation_date
        if creator is not unset:
            kwargs["creator"] = creator
        if default_rule is not unset:
            kwargs["default_rule"] = default_rule
        if description is not unset:
            kwargs["description"] = description
        if enabled is not unset:
            kwargs["enabled"] = enabled
        if expression is not unset:
            kwargs["expression"] = expression
        if name is not unset:
            kwargs["name"] = name
        if updated_at is not unset:
            kwargs["updated_at"] = updated_at
        if updater is not unset:
            kwargs["updater"] = updater
        if version is not unset:
            kwargs["version"] = version
        super().__init__(kwargs)
