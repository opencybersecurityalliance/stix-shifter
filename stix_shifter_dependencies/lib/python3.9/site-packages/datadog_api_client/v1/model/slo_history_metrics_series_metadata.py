# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import List, Union, TYPE_CHECKING

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    none_type,
    unset,
    UnsetType,
)


if TYPE_CHECKING:
    from datadog_api_client.v1.model.slo_history_metrics_series_metadata_unit import SLOHistoryMetricsSeriesMetadataUnit


class SLOHistoryMetricsSeriesMetadata(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.slo_history_metrics_series_metadata_unit import (
            SLOHistoryMetricsSeriesMetadataUnit,
        )

        return {
            "aggr": (str,),
            "expression": (str,),
            "metric": (str,),
            "query_index": (int,),
            "scope": (str,),
            "unit": ([SLOHistoryMetricsSeriesMetadataUnit, none_type], none_type),
        }

    attribute_map = {
        "aggr": "aggr",
        "expression": "expression",
        "metric": "metric",
        "query_index": "query_index",
        "scope": "scope",
        "unit": "unit",
    }

    def __init__(
        self_,
        aggr: Union[str, UnsetType] = unset,
        expression: Union[str, UnsetType] = unset,
        metric: Union[str, UnsetType] = unset,
        query_index: Union[int, UnsetType] = unset,
        scope: Union[str, UnsetType] = unset,
        unit: Union[List[SLOHistoryMetricsSeriesMetadataUnit], none_type, UnsetType] = unset,
        **kwargs,
    ):
        """
        Query metadata.

        :param aggr: Query aggregator function.
        :type aggr: str, optional

        :param expression: Query expression.
        :type expression: str, optional

        :param metric: Query metric used.
        :type metric: str, optional

        :param query_index: Query index from original combined query.
        :type query_index: int, optional

        :param scope: Query scope.
        :type scope: str, optional

        :param unit: An array of metric units that contains up to two unit objects.
            For example, bytes represents one unit object and bytes per second represents two unit objects.
            If a metric query only has one unit object, the second array element is null.
        :type unit: [SLOHistoryMetricsSeriesMetadataUnit, none_type], none_type, optional
        """
        if aggr is not unset:
            kwargs["aggr"] = aggr
        if expression is not unset:
            kwargs["expression"] = expression
        if metric is not unset:
            kwargs["metric"] = metric
        if query_index is not unset:
            kwargs["query_index"] = query_index
        if scope is not unset:
            kwargs["scope"] = scope
        if unit is not unset:
            kwargs["unit"] = unit
        super().__init__(kwargs)
