# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class FormulaAndFunctionApmDependencyStatsDataSource(ModelSimple):
    """
    Data source for APM dependency stats queries.

    :param value: If omitted defaults to "apm_dependency_stats". Must be one of ["apm_dependency_stats"].
    :type value: str
    """

    allowed_values = {
        "apm_dependency_stats",
    }
    APM_DEPENDENCY_STATS: ClassVar["FormulaAndFunctionApmDependencyStatsDataSource"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


FormulaAndFunctionApmDependencyStatsDataSource.APM_DEPENDENCY_STATS = FormulaAndFunctionApmDependencyStatsDataSource(
    "apm_dependency_stats"
)
