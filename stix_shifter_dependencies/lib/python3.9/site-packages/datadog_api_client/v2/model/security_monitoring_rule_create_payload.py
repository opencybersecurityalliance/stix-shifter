# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelComposed,
    cached_property,
)


class SecurityMonitoringRuleCreatePayload(ModelComposed):
    def __init__(self, **kwargs):
        """
        Create a new rule.

        :param cases: Cases for generating signals.
        :type cases: [SecurityMonitoringRuleCaseCreate]

        :param filters: Additional queries to filter matched events before they are processed.
        :type filters: [SecurityMonitoringFilter], optional

        :param has_extended_title: Whether the notifications include the triggering group-by values in their title.
        :type has_extended_title: bool, optional

        :param is_enabled: Whether the rule is enabled.
        :type is_enabled: bool

        :param message: Message for generated signals.
        :type message: str

        :param name: The name of the rule.
        :type name: str

        :param options: Options on rules.
        :type options: SecurityMonitoringRuleOptions

        :param queries: Queries for selecting logs which are part of the rule.
        :type queries: [SecurityMonitoringStandardRuleQuery]

        :param tags: Tags for generated signals.
        :type tags: [str], optional

        :param type: The rule type.
        :type type: SecurityMonitoringRuleTypeCreate, optional

        :param compliance_signal_options: How to generate compliance signals. Useful for cloud_configuration rules only.
        :type compliance_signal_options: CloudConfigurationRuleComplianceSignalOptions
        """
        super().__init__(kwargs)

    @cached_property
    def _composed_schemas(_):
        # we need this here to make our import statements work
        # we must store _composed_schemas in here so the code is only run
        # when we invoke this method. If we kept this at the class
        # level we would get an error because the class level
        # code would be run when this module is imported, and these composed
        # classes don't exist yet because their module has not finished
        # loading
        from datadog_api_client.v2.model.security_monitoring_standard_rule_create_payload import (
            SecurityMonitoringStandardRuleCreatePayload,
        )
        from datadog_api_client.v2.model.security_monitoring_signal_rule_create_payload import (
            SecurityMonitoringSignalRuleCreatePayload,
        )
        from datadog_api_client.v2.model.cloud_configuration_rule_create_payload import (
            CloudConfigurationRuleCreatePayload,
        )

        return {
            "oneOf": [
                SecurityMonitoringStandardRuleCreatePayload,
                SecurityMonitoringSignalRuleCreatePayload,
                CloudConfigurationRuleCreatePayload,
            ],
        }
