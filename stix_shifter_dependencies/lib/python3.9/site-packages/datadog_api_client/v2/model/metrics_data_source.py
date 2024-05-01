# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class MetricsDataSource(ModelSimple):
    """
    A data source that is powered by the Metrics platform.

    :param value: If omitted defaults to "metrics". Must be one of ["metrics", "cloud_cost"].
    :type value: str
    """

    allowed_values = {
        "metrics",
        "cloud_cost",
    }
    METRICS: ClassVar["MetricsDataSource"]
    CLOUD_COST: ClassVar["MetricsDataSource"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


MetricsDataSource.METRICS = MetricsDataSource("metrics")
MetricsDataSource.CLOUD_COST = MetricsDataSource("cloud_cost")
