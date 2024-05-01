# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import List, Union, TYPE_CHECKING

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    unset,
    UnsetType,
)


if TYPE_CHECKING:
    from datadog_api_client.v1.model.slo_history_metrics_series_metadata import SLOHistoryMetricsSeriesMetadata


class SLOHistoryMetricsSeries(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.slo_history_metrics_series_metadata import SLOHistoryMetricsSeriesMetadata

        return {
            "count": (int,),
            "metadata": (SLOHistoryMetricsSeriesMetadata,),
            "sum": (float,),
            "values": ([float],),
        }

    attribute_map = {
        "count": "count",
        "metadata": "metadata",
        "sum": "sum",
        "values": "values",
    }

    def __init__(
        self_,
        count: int,
        sum: float,
        values: List[float],
        metadata: Union[SLOHistoryMetricsSeriesMetadata, UnsetType] = unset,
        **kwargs,
    ):
        """
        A representation of ``metric`` based SLO time series for the provided queries.
        This is the same response type from ``batch_query`` endpoint.

        :param count: Count of submitted metrics.
        :type count: int

        :param metadata: Query metadata.
        :type metadata: SLOHistoryMetricsSeriesMetadata, optional

        :param sum: Total sum of the query.
        :type sum: float

        :param values: The query values for each metric.
        :type values: [float]
        """
        if metadata is not unset:
            kwargs["metadata"] = metadata
        super().__init__(kwargs)

        self_.count = count
        self_.sum = sum
        self_.values = values
