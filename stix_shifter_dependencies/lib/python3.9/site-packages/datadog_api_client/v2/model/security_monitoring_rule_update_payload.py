# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import List, Union, TYPE_CHECKING

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    unset,
    UnsetType,
)


if TYPE_CHECKING:
    from datadog_api_client.v2.model.security_monitoring_rule_case import SecurityMonitoringRuleCase
    from datadog_api_client.v2.model.cloud_configuration_rule_compliance_signal_options import (
        CloudConfigurationRuleComplianceSignalOptions,
    )
    from datadog_api_client.v2.model.security_monitoring_filter import SecurityMonitoringFilter
    from datadog_api_client.v2.model.security_monitoring_rule_options import SecurityMonitoringRuleOptions
    from datadog_api_client.v2.model.security_monitoring_rule_query import SecurityMonitoringRuleQuery
    from datadog_api_client.v2.model.security_monitoring_standard_rule_query import SecurityMonitoringStandardRuleQuery
    from datadog_api_client.v2.model.security_monitoring_signal_rule_query import SecurityMonitoringSignalRuleQuery


class SecurityMonitoringRuleUpdatePayload(ModelNormal):
    validations = {
        "version": {
            "inclusive_maximum": 2147483647,
        },
    }

    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.security_monitoring_rule_case import SecurityMonitoringRuleCase
        from datadog_api_client.v2.model.cloud_configuration_rule_compliance_signal_options import (
            CloudConfigurationRuleComplianceSignalOptions,
        )
        from datadog_api_client.v2.model.security_monitoring_filter import SecurityMonitoringFilter
        from datadog_api_client.v2.model.security_monitoring_rule_options import SecurityMonitoringRuleOptions
        from datadog_api_client.v2.model.security_monitoring_rule_query import SecurityMonitoringRuleQuery

        return {
            "cases": ([SecurityMonitoringRuleCase],),
            "compliance_signal_options": (CloudConfigurationRuleComplianceSignalOptions,),
            "filters": ([SecurityMonitoringFilter],),
            "has_extended_title": (bool,),
            "is_enabled": (bool,),
            "message": (str,),
            "name": (str,),
            "options": (SecurityMonitoringRuleOptions,),
            "queries": ([SecurityMonitoringRuleQuery],),
            "tags": ([str],),
            "version": (int,),
        }

    attribute_map = {
        "cases": "cases",
        "compliance_signal_options": "complianceSignalOptions",
        "filters": "filters",
        "has_extended_title": "hasExtendedTitle",
        "is_enabled": "isEnabled",
        "message": "message",
        "name": "name",
        "options": "options",
        "queries": "queries",
        "tags": "tags",
        "version": "version",
    }

    def __init__(
        self_,
        cases: Union[List[SecurityMonitoringRuleCase], UnsetType] = unset,
        compliance_signal_options: Union[CloudConfigurationRuleComplianceSignalOptions, UnsetType] = unset,
        filters: Union[List[SecurityMonitoringFilter], UnsetType] = unset,
        has_extended_title: Union[bool, UnsetType] = unset,
        is_enabled: Union[bool, UnsetType] = unset,
        message: Union[str, UnsetType] = unset,
        name: Union[str, UnsetType] = unset,
        options: Union[SecurityMonitoringRuleOptions, UnsetType] = unset,
        queries: Union[
            List[
                Union[
                    SecurityMonitoringRuleQuery, SecurityMonitoringStandardRuleQuery, SecurityMonitoringSignalRuleQuery
                ]
            ],
            UnsetType,
        ] = unset,
        tags: Union[List[str], UnsetType] = unset,
        version: Union[int, UnsetType] = unset,
        **kwargs,
    ):
        """
        Update an existing rule.

        :param cases: Cases for generating signals.
        :type cases: [SecurityMonitoringRuleCase], optional

        :param compliance_signal_options: How to generate compliance signals. Useful for cloud_configuration rules only.
        :type compliance_signal_options: CloudConfigurationRuleComplianceSignalOptions, optional

        :param filters: Additional queries to filter matched events before they are processed.
        :type filters: [SecurityMonitoringFilter], optional

        :param has_extended_title: Whether the notifications include the triggering group-by values in their title.
        :type has_extended_title: bool, optional

        :param is_enabled: Whether the rule is enabled.
        :type is_enabled: bool, optional

        :param message: Message for generated signals.
        :type message: str, optional

        :param name: Name of the rule.
        :type name: str, optional

        :param options: Options on rules.
        :type options: SecurityMonitoringRuleOptions, optional

        :param queries: Queries for selecting logs which are part of the rule.
        :type queries: [SecurityMonitoringRuleQuery], optional

        :param tags: Tags for generated signals.
        :type tags: [str], optional

        :param version: The version of the rule being updated.
        :type version: int, optional
        """
        if cases is not unset:
            kwargs["cases"] = cases
        if compliance_signal_options is not unset:
            kwargs["compliance_signal_options"] = compliance_signal_options
        if filters is not unset:
            kwargs["filters"] = filters
        if has_extended_title is not unset:
            kwargs["has_extended_title"] = has_extended_title
        if is_enabled is not unset:
            kwargs["is_enabled"] = is_enabled
        if message is not unset:
            kwargs["message"] = message
        if name is not unset:
            kwargs["name"] = name
        if options is not unset:
            kwargs["options"] = options
        if queries is not unset:
            kwargs["queries"] = queries
        if tags is not unset:
            kwargs["tags"] = tags
        if version is not unset:
            kwargs["version"] = version
        super().__init__(kwargs)
