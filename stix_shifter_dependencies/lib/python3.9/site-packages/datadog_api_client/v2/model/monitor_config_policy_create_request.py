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
    from datadog_api_client.v2.model.monitor_config_policy_create_data import MonitorConfigPolicyCreateData


class MonitorConfigPolicyCreateRequest(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.monitor_config_policy_create_data import MonitorConfigPolicyCreateData

        return {
            "data": (MonitorConfigPolicyCreateData,),
        }

    attribute_map = {
        "data": "data",
    }

    def __init__(self_, data: MonitorConfigPolicyCreateData, **kwargs):
        """
        Request for creating a monitor configuration policy.

        :param data: A monitor configuration policy data.
        :type data: MonitorConfigPolicyCreateData
        """
        super().__init__(kwargs)

        self_.data = data
