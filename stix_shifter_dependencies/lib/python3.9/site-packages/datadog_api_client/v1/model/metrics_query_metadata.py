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
    from datadog_api_client.v1.model.point import Point
    from datadog_api_client.v1.model.metrics_query_unit import MetricsQueryUnit


class MetricsQueryMetadata(ModelNormal):
    validations = {
        "unit": {
            "max_items": 2,
            "min_items": 2,
        },
    }

    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.point import Point
        from datadog_api_client.v1.model.metrics_query_unit import MetricsQueryUnit

        return {
            "aggr": (str, none_type),
            "display_name": (str,),
            "end": (int,),
            "expression": (str,),
            "interval": (int,),
            "length": (int,),
            "metric": (str,),
            "pointlist": ([Point],),
            "query_index": (int,),
            "scope": (str,),
            "start": (int,),
            "tag_set": ([str],),
            "unit": ([MetricsQueryUnit, none_type],),
        }

    attribute_map = {
        "aggr": "aggr",
        "display_name": "display_name",
        "end": "end",
        "expression": "expression",
        "interval": "interval",
        "length": "length",
        "metric": "metric",
        "pointlist": "pointlist",
        "query_index": "query_index",
        "scope": "scope",
        "start": "start",
        "tag_set": "tag_set",
        "unit": "unit",
    }
    read_only_vars = {
        "aggr",
        "display_name",
        "end",
        "expression",
        "interval",
        "length",
        "metric",
        "pointlist",
        "query_index",
        "scope",
        "start",
        "tag_set",
        "unit",
    }

    def __init__(
        self_,
        aggr: Union[str, none_type, UnsetType] = unset,
        display_name: Union[str, UnsetType] = unset,
        end: Union[int, UnsetType] = unset,
        expression: Union[str, UnsetType] = unset,
        interval: Union[int, UnsetType] = unset,
        length: Union[int, UnsetType] = unset,
        metric: Union[str, UnsetType] = unset,
        pointlist: Union[List[Point], UnsetType] = unset,
        query_index: Union[int, UnsetType] = unset,
        scope: Union[str, UnsetType] = unset,
        start: Union[int, UnsetType] = unset,
        tag_set: Union[List[str], UnsetType] = unset,
        unit: Union[List[MetricsQueryUnit], UnsetType] = unset,
        **kwargs,
    ):
        """
        Object containing all metric names returned and their associated metadata.

        :param aggr: Aggregation type.
        :type aggr: str, none_type, optional

        :param display_name: Display name of the metric.
        :type display_name: str, optional

        :param end: End of the time window, milliseconds since Unix epoch.
        :type end: int, optional

        :param expression: Metric expression.
        :type expression: str, optional

        :param interval: Number of milliseconds between data samples.
        :type interval: int, optional

        :param length: Number of data samples.
        :type length: int, optional

        :param metric: Metric name.
        :type metric: str, optional

        :param pointlist: List of points of the time series in milliseconds.
        :type pointlist: [Point], optional

        :param query_index: The index of the series' query within the request.
        :type query_index: int, optional

        :param scope: Metric scope, comma separated list of tags.
        :type scope: str, optional

        :param start: Start of the time window, milliseconds since Unix epoch.
        :type start: int, optional

        :param tag_set: Unique tags identifying this series.
        :type tag_set: [str], optional

        :param unit: Detailed information about the metric unit.
            The first element describes the "primary unit" (for example, ``bytes`` in ``bytes per second`` ).
            The second element describes the "per unit" (for example, ``second`` in ``bytes per second`` ).
            If the second element is not present, the API returns null.
        :type unit: [MetricsQueryUnit, none_type], optional
        """
        if aggr is not unset:
            kwargs["aggr"] = aggr
        if display_name is not unset:
            kwargs["display_name"] = display_name
        if end is not unset:
            kwargs["end"] = end
        if expression is not unset:
            kwargs["expression"] = expression
        if interval is not unset:
            kwargs["interval"] = interval
        if length is not unset:
            kwargs["length"] = length
        if metric is not unset:
            kwargs["metric"] = metric
        if pointlist is not unset:
            kwargs["pointlist"] = pointlist
        if query_index is not unset:
            kwargs["query_index"] = query_index
        if scope is not unset:
            kwargs["scope"] = scope
        if start is not unset:
            kwargs["start"] = start
        if tag_set is not unset:
            kwargs["tag_set"] = tag_set
        if unit is not unset:
            kwargs["unit"] = unit
        super().__init__(kwargs)
