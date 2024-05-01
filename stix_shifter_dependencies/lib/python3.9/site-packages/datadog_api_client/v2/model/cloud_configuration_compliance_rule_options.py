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
    from datadog_api_client.v2.model.cloud_configuration_rego_rule import CloudConfigurationRegoRule


class CloudConfigurationComplianceRuleOptions(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.cloud_configuration_rego_rule import CloudConfigurationRegoRule

        return {
            "complex_rule": (bool,),
            "rego_rule": (CloudConfigurationRegoRule,),
            "resource_type": (str,),
        }

    attribute_map = {
        "complex_rule": "complexRule",
        "rego_rule": "regoRule",
        "resource_type": "resourceType",
    }

    def __init__(
        self_,
        complex_rule: Union[bool, UnsetType] = unset,
        rego_rule: Union[CloudConfigurationRegoRule, UnsetType] = unset,
        resource_type: Union[str, UnsetType] = unset,
        **kwargs,
    ):
        """
        Options for cloud_configuration rules.
        Fields ``resourceType`` and ``regoRule`` are mandatory when managing custom ``cloud_configuration`` rules.

        :param complex_rule: Whether the rule is a complex one.
            Must be set to true if ``regoRule.resourceTypes`` contains more than one item. Defaults to false.
        :type complex_rule: bool, optional

        :param rego_rule: Rule details.
        :type rego_rule: CloudConfigurationRegoRule, optional

        :param resource_type: Main resource type to be checked by the rule. It should be specified again in ``regoRule.resourceTypes``.
        :type resource_type: str, optional
        """
        if complex_rule is not unset:
            kwargs["complex_rule"] = complex_rule
        if rego_rule is not unset:
            kwargs["rego_rule"] = rego_rule
        if resource_type is not unset:
            kwargs["resource_type"] = resource_type
        super().__init__(kwargs)
