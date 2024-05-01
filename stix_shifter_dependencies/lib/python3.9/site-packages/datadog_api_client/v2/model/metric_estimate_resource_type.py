# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class MetricEstimateResourceType(ModelSimple):
    """
    The metric estimate resource type.

    :param value: If omitted defaults to "metric_cardinality_estimate". Must be one of ["metric_cardinality_estimate"].
    :type value: str
    """

    allowed_values = {
        "metric_cardinality_estimate",
    }
    METRIC_CARDINALITY_ESTIMATE: ClassVar["MetricEstimateResourceType"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


MetricEstimateResourceType.METRIC_CARDINALITY_ESTIMATE = MetricEstimateResourceType("metric_cardinality_estimate")
