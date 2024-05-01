# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Union, TYPE_CHECKING

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
)


if TYPE_CHECKING:
    from datadog_api_client.v2.model.monitor_config_policy_policy import MonitorConfigPolicyPolicy
    from datadog_api_client.v2.model.monitor_config_policy_type import MonitorConfigPolicyType
    from datadog_api_client.v2.model.monitor_config_policy_tag_policy import MonitorConfigPolicyTagPolicy


class MonitorConfigPolicyAttributeEditRequest(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.monitor_config_policy_policy import MonitorConfigPolicyPolicy
        from datadog_api_client.v2.model.monitor_config_policy_type import MonitorConfigPolicyType

        return {
            "policy": (MonitorConfigPolicyPolicy,),
            "policy_type": (MonitorConfigPolicyType,),
        }

    attribute_map = {
        "policy": "policy",
        "policy_type": "policy_type",
    }

    def __init__(
        self_,
        policy: Union[MonitorConfigPolicyPolicy, MonitorConfigPolicyTagPolicy],
        policy_type: MonitorConfigPolicyType,
        **kwargs,
    ):
        """
        Policy and policy type for a monitor configuration policy.

        :param policy: Configuration for the policy.
        :type policy: MonitorConfigPolicyPolicy

        :param policy_type: The monitor configuration policy type.
        :type policy_type: MonitorConfigPolicyType
        """
        super().__init__(kwargs)

        self_.policy = policy
        self_.policy_type = policy_type
