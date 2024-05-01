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
    from datadog_api_client.v2.model.cloud_workload_security_agent_rule_create_data import (
        CloudWorkloadSecurityAgentRuleCreateData,
    )


class CloudWorkloadSecurityAgentRuleCreateRequest(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.cloud_workload_security_agent_rule_create_data import (
            CloudWorkloadSecurityAgentRuleCreateData,
        )

        return {
            "data": (CloudWorkloadSecurityAgentRuleCreateData,),
        }

    attribute_map = {
        "data": "data",
    }

    def __init__(self_, data: CloudWorkloadSecurityAgentRuleCreateData, **kwargs):
        """
        Request object that includes the Agent rule to create.

        :param data: Object for a single Agent rule.
        :type data: CloudWorkloadSecurityAgentRuleCreateData
        """
        super().__init__(kwargs)

        self_.data = data
