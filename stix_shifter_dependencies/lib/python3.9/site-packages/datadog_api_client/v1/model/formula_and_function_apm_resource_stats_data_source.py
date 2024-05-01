# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class FormulaAndFunctionApmResourceStatsDataSource(ModelSimple):
    """
    Data source for APM resource stats queries.

    :param value: If omitted defaults to "apm_resource_stats". Must be one of ["apm_resource_stats"].
    :type value: str
    """

    allowed_values = {
        "apm_resource_stats",
    }
    APM_RESOURCE_STATS: ClassVar["FormulaAndFunctionApmResourceStatsDataSource"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


FormulaAndFunctionApmResourceStatsDataSource.APM_RESOURCE_STATS = FormulaAndFunctionApmResourceStatsDataSource(
    "apm_resource_stats"
)
