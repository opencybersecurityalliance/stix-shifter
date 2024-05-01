# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class FormulaAndFunctionMetricDataSource(ModelSimple):
    """
    Data source for metrics queries.

    :param value: If omitted defaults to "metrics". Must be one of ["metrics"].
    :type value: str
    """

    allowed_values = {
        "metrics",
    }
    METRICS: ClassVar["FormulaAndFunctionMetricDataSource"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


FormulaAndFunctionMetricDataSource.METRICS = FormulaAndFunctionMetricDataSource("metrics")
