# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class FormulaAndFunctionApmResourceStatName(ModelSimple):
    """
    APM resource stat name.

    :param value: Must be one of ["errors", "error_rate", "hits", "latency_avg", "latency_distribution", "latency_max", "latency_p50", "latency_p75", "latency_p90", "latency_p95", "latency_p99"].
    :type value: str
    """

    allowed_values = {
        "errors",
        "error_rate",
        "hits",
        "latency_avg",
        "latency_distribution",
        "latency_max",
        "latency_p50",
        "latency_p75",
        "latency_p90",
        "latency_p95",
        "latency_p99",
    }
    ERRORS: ClassVar["FormulaAndFunctionApmResourceStatName"]
    ERROR_RATE: ClassVar["FormulaAndFunctionApmResourceStatName"]
    HITS: ClassVar["FormulaAndFunctionApmResourceStatName"]
    LATENCY_AVG: ClassVar["FormulaAndFunctionApmResourceStatName"]
    LATENCY_DISTRIBUTION: ClassVar["FormulaAndFunctionApmResourceStatName"]
    LATENCY_MAX: ClassVar["FormulaAndFunctionApmResourceStatName"]
    LATENCY_P50: ClassVar["FormulaAndFunctionApmResourceStatName"]
    LATENCY_P75: ClassVar["FormulaAndFunctionApmResourceStatName"]
    LATENCY_P90: ClassVar["FormulaAndFunctionApmResourceStatName"]
    LATENCY_P95: ClassVar["FormulaAndFunctionApmResourceStatName"]
    LATENCY_P99: ClassVar["FormulaAndFunctionApmResourceStatName"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


FormulaAndFunctionApmResourceStatName.ERRORS = FormulaAndFunctionApmResourceStatName("errors")
FormulaAndFunctionApmResourceStatName.ERROR_RATE = FormulaAndFunctionApmResourceStatName("error_rate")
FormulaAndFunctionApmResourceStatName.HITS = FormulaAndFunctionApmResourceStatName("hits")
FormulaAndFunctionApmResourceStatName.LATENCY_AVG = FormulaAndFunctionApmResourceStatName("latency_avg")
FormulaAndFunctionApmResourceStatName.LATENCY_DISTRIBUTION = FormulaAndFunctionApmResourceStatName(
    "latency_distribution"
)
FormulaAndFunctionApmResourceStatName.LATENCY_MAX = FormulaAndFunctionApmResourceStatName("latency_max")
FormulaAndFunctionApmResourceStatName.LATENCY_P50 = FormulaAndFunctionApmResourceStatName("latency_p50")
FormulaAndFunctionApmResourceStatName.LATENCY_P75 = FormulaAndFunctionApmResourceStatName("latency_p75")
FormulaAndFunctionApmResourceStatName.LATENCY_P90 = FormulaAndFunctionApmResourceStatName("latency_p90")
FormulaAndFunctionApmResourceStatName.LATENCY_P95 = FormulaAndFunctionApmResourceStatName("latency_p95")
FormulaAndFunctionApmResourceStatName.LATENCY_P99 = FormulaAndFunctionApmResourceStatName("latency_p99")
