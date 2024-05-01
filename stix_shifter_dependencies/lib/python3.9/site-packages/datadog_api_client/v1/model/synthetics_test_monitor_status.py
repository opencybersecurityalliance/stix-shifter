# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class SyntheticsTestMonitorStatus(ModelSimple):
    """
    The status of your Synthetic monitor.
        * `O` for not triggered
        * `1` for triggered
        * `2` for no data

    :param value: Must be one of [0, 1, 2].
    :type value: int
    """

    allowed_values = {
        0,
        1,
        2,
    }
    UNTRIGGERED: ClassVar["SyntheticsTestMonitorStatus"]
    TRIGGERED: ClassVar["SyntheticsTestMonitorStatus"]
    NO_DATA: ClassVar["SyntheticsTestMonitorStatus"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (int,),
        }


SyntheticsTestMonitorStatus.UNTRIGGERED = SyntheticsTestMonitorStatus(0)
SyntheticsTestMonitorStatus.TRIGGERED = SyntheticsTestMonitorStatus(1)
SyntheticsTestMonitorStatus.NO_DATA = SyntheticsTestMonitorStatus(2)
