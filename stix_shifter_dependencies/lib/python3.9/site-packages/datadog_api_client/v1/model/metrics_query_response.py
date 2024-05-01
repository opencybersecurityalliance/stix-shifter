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
    from datadog_api_client.v1.model.metrics_query_metadata import MetricsQueryMetadata


class MetricsQueryResponse(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.metrics_query_metadata import MetricsQueryMetadata

        return {
            "error": (str,),
            "from_date": (int,),
            "group_by": ([str],),
            "message": (str,),
            "query": (str,),
            "res_type": (str,),
            "series": ([MetricsQueryMetadata],),
            "status": (str,),
            "to_date": (int,),
        }

    attribute_map = {
        "error": "error",
        "from_date": "from_date",
        "group_by": "group_by",
        "message": "message",
        "query": "query",
        "res_type": "res_type",
        "series": "series",
        "status": "status",
        "to_date": "to_date",
    }
    read_only_vars = {
        "error",
        "from_date",
        "group_by",
        "message",
        "query",
        "res_type",
        "series",
        "status",
        "to_date",
    }

    def __init__(
        self_,
        error: Union[str, UnsetType] = unset,
        from_date: Union[int, UnsetType] = unset,
        group_by: Union[List[str], UnsetType] = unset,
        message: Union[str, UnsetType] = unset,
        query: Union[str, UnsetType] = unset,
        res_type: Union[str, UnsetType] = unset,
        series: Union[List[MetricsQueryMetadata], UnsetType] = unset,
        status: Union[str, UnsetType] = unset,
        to_date: Union[int, UnsetType] = unset,
        **kwargs,
    ):
        """
        Response Object that includes your query and the list of metrics retrieved.

        :param error: Message indicating the errors if status is not ``ok``.
        :type error: str, optional

        :param from_date: Start of requested time window, milliseconds since Unix epoch.
        :type from_date: int, optional

        :param group_by: List of tag keys on which to group.
        :type group_by: [str], optional

        :param message: Message indicating ``success`` if status is ``ok``.
        :type message: str, optional

        :param query: Query string
        :type query: str, optional

        :param res_type: Type of response.
        :type res_type: str, optional

        :param series: List of timeseries queried.
        :type series: [MetricsQueryMetadata], optional

        :param status: Status of the query.
        :type status: str, optional

        :param to_date: End of requested time window, milliseconds since Unix epoch.
        :type to_date: int, optional
        """
        if error is not unset:
            kwargs["error"] = error
        if from_date is not unset:
            kwargs["from_date"] = from_date
        if group_by is not unset:
            kwargs["group_by"] = group_by
        if message is not unset:
            kwargs["message"] = message
        if query is not unset:
            kwargs["query"] = query
        if res_type is not unset:
            kwargs["res_type"] = res_type
        if series is not unset:
            kwargs["series"] = series
        if status is not unset:
            kwargs["status"] = status
        if to_date is not unset:
            kwargs["to_date"] = to_date
        super().__init__(kwargs)
