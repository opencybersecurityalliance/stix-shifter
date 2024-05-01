# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class MetricCustomSpaceAggregation(ModelSimple):
    """
    A space aggregation for use in query.

    :param value: Must be one of ["avg", "max", "min", "sum"].
    :type value: str
    """

    allowed_values = {
        "avg",
        "max",
        "min",
        "sum",
    }
    AVG: ClassVar["MetricCustomSpaceAggregation"]
    MAX: ClassVar["MetricCustomSpaceAggregation"]
    MIN: ClassVar["MetricCustomSpaceAggregation"]
    SUM: ClassVar["MetricCustomSpaceAggregation"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


MetricCustomSpaceAggregation.AVG = MetricCustomSpaceAggregation("avg")
MetricCustomSpaceAggregation.MAX = MetricCustomSpaceAggregation("max")
MetricCustomSpaceAggregation.MIN = MetricCustomSpaceAggregation("min")
MetricCustomSpaceAggregation.SUM = MetricCustomSpaceAggregation("sum")
