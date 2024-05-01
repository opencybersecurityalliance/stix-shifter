# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import TYPE_CHECKING

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
)


if TYPE_CHECKING:
    from datadog_api_client.v2.model.cloud_configuration_compliance_rule_options import (
        CloudConfigurationComplianceRuleOptions,
    )


class CloudConfigurationRuleOptions(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.cloud_configuration_compliance_rule_options import (
            CloudConfigurationComplianceRuleOptions,
        )

        return {
            "compliance_rule_options": (CloudConfigurationComplianceRuleOptions,),
        }

    attribute_map = {
        "compliance_rule_options": "complianceRuleOptions",
    }

    def __init__(self_, compliance_rule_options: CloudConfigurationComplianceRuleOptions, **kwargs):
        """
        Options on cloud configuration rules.

        :param compliance_rule_options: Options for cloud_configuration rules.
            Fields ``resourceType`` and ``regoRule`` are mandatory when managing custom ``cloud_configuration`` rules.
        :type compliance_rule_options: CloudConfigurationComplianceRuleOptions
        """
        super().__init__(kwargs)

        self_.compliance_rule_options = compliance_rule_options
