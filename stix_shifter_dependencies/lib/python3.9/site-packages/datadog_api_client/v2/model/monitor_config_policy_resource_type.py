# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class MonitorConfigPolicyResourceType(ModelSimple):
    """
    Monitor configuration policy resource type.

    :param value: If omitted defaults to "monitor-config-policy". Must be one of ["monitor-config-policy"].
    :type value: str
    """

    allowed_values = {
        "monitor-config-policy",
    }
    MONITOR_CONFIG_POLICY: ClassVar["MonitorConfigPolicyResourceType"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


MonitorConfigPolicyResourceType.MONITOR_CONFIG_POLICY = MonitorConfigPolicyResourceType("monitor-config-policy")
