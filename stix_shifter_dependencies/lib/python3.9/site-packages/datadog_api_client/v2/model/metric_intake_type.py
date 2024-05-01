# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class MetricIntakeType(ModelSimple):
    """
    The type of metric. The available types are `0` (unspecified), `1` (count), `2` (rate), and `3` (gauge).

    :param value: Must be one of [0, 1, 2, 3].
    :type value: int
    """

    allowed_values = {
        0,
        1,
        2,
        3,
    }
    UNSPECIFIED: ClassVar["MetricIntakeType"]
    COUNT: ClassVar["MetricIntakeType"]
    RATE: ClassVar["MetricIntakeType"]
    GAUGE: ClassVar["MetricIntakeType"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (int,),
        }


MetricIntakeType.UNSPECIFIED = MetricIntakeType(0)
MetricIntakeType.COUNT = MetricIntakeType(1)
MetricIntakeType.RATE = MetricIntakeType(2)
MetricIntakeType.GAUGE = MetricIntakeType(3)
