# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class FormulaAndFunctionApmDependencyStatName(ModelSimple):
    """
    APM statistic.

    :param value: Must be one of ["avg_duration", "avg_root_duration", "avg_spans_per_trace", "error_rate", "pct_exec_time", "pct_of_traces", "total_traces_count"].
    :type value: str
    """

    allowed_values = {
        "avg_duration",
        "avg_root_duration",
        "avg_spans_per_trace",
        "error_rate",
        "pct_exec_time",
        "pct_of_traces",
        "total_traces_count",
    }
    AVG_DURATION: ClassVar["FormulaAndFunctionApmDependencyStatName"]
    AVG_ROOT_DURATION: ClassVar["FormulaAndFunctionApmDependencyStatName"]
    AVG_SPANS_PER_TRACE: ClassVar["FormulaAndFunctionApmDependencyStatName"]
    ERROR_RATE: ClassVar["FormulaAndFunctionApmDependencyStatName"]
    PCT_EXEC_TIME: ClassVar["FormulaAndFunctionApmDependencyStatName"]
    PCT_OF_TRACES: ClassVar["FormulaAndFunctionApmDependencyStatName"]
    TOTAL_TRACES_COUNT: ClassVar["FormulaAndFunctionApmDependencyStatName"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


FormulaAndFunctionApmDependencyStatName.AVG_DURATION = FormulaAndFunctionApmDependencyStatName("avg_duration")
FormulaAndFunctionApmDependencyStatName.AVG_ROOT_DURATION = FormulaAndFunctionApmDependencyStatName("avg_root_duration")
FormulaAndFunctionApmDependencyStatName.AVG_SPANS_PER_TRACE = FormulaAndFunctionApmDependencyStatName(
    "avg_spans_per_trace"
)
FormulaAndFunctionApmDependencyStatName.ERROR_RATE = FormulaAndFunctionApmDependencyStatName("error_rate")
FormulaAndFunctionApmDependencyStatName.PCT_EXEC_TIME = FormulaAndFunctionApmDependencyStatName("pct_exec_time")
FormulaAndFunctionApmDependencyStatName.PCT_OF_TRACES = FormulaAndFunctionApmDependencyStatName("pct_of_traces")
FormulaAndFunctionApmDependencyStatName.TOTAL_TRACES_COUNT = FormulaAndFunctionApmDependencyStatName(
    "total_traces_count"
)
