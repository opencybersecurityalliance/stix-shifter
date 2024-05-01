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
    from datadog_api_client.v2.model.monitor_config_policy_policy import MonitorConfigPolicyPolicy
    from datadog_api_client.v2.model.monitor_config_policy_type import MonitorConfigPolicyType
    from datadog_api_client.v2.model.monitor_config_policy_tag_policy import MonitorConfigPolicyTagPolicy


class MonitorConfigPolicyAttributeResponse(ModelNormal):
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
        policy: Union[MonitorConfigPolicyPolicy, MonitorConfigPolicyTagPolicy, UnsetType] = unset,
        policy_type: Union[MonitorConfigPolicyType, UnsetType] = unset,
        **kwargs,
    ):
        """
        Policy and policy type for a monitor configuration policy.

        :param policy: Configuration for the policy.
        :type policy: MonitorConfigPolicyPolicy, optional

        :param policy_type: The monitor configuration policy type.
        :type policy_type: MonitorConfigPolicyType, optional
        """
        if policy is not unset:
            kwargs["policy"] = policy
        if policy_type is not unset:
            kwargs["policy_type"] = policy_type
        super().__init__(kwargs)
