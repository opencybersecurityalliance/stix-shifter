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
    from datadog_api_client.v2.model.cloud_workload_security_agent_rule_data import CloudWorkloadSecurityAgentRuleData


class CloudWorkloadSecurityAgentRuleResponse(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.cloud_workload_security_agent_rule_data import (
            CloudWorkloadSecurityAgentRuleData,
        )

        return {
            "data": (CloudWorkloadSecurityAgentRuleData,),
        }

    attribute_map = {
        "data": "data",
    }

    def __init__(self_, data: Union[CloudWorkloadSecurityAgentRuleData, UnsetType] = unset, **kwargs):
        """
        Response object that includes an Agent rule.

        :param data: Object for a single Agent rule.
        :type data: CloudWorkloadSecurityAgentRuleData, optional
        """
        if data is not unset:
            kwargs["data"] = data
        super().__init__(kwargs)
