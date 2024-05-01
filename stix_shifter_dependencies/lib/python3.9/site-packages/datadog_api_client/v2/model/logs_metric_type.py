# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class LogsMetricType(ModelSimple):
    """
    The type of the resource. The value should always be logs_metrics.

    :param value: If omitted defaults to "logs_metrics". Must be one of ["logs_metrics"].
    :type value: str
    """

    allowed_values = {
        "logs_metrics",
    }
    LOGS_METRICS: ClassVar["LogsMetricType"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


LogsMetricType.LOGS_METRICS = LogsMetricType("logs_metrics")
