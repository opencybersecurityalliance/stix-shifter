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
    from datadog_api_client.v1.model.logs_query_compute import LogsQueryCompute
    from datadog_api_client.v1.model.log_query_definition_group_by import LogQueryDefinitionGroupBy
    from datadog_api_client.v1.model.log_query_definition_search import LogQueryDefinitionSearch


class LogQueryDefinition(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.logs_query_compute import LogsQueryCompute
        from datadog_api_client.v1.model.log_query_definition_group_by import LogQueryDefinitionGroupBy
        from datadog_api_client.v1.model.log_query_definition_search import LogQueryDefinitionSearch

        return {
            "compute": (LogsQueryCompute,),
            "group_by": ([LogQueryDefinitionGroupBy],),
            "index": (str,),
            "multi_compute": ([LogsQueryCompute],),
            "search": (LogQueryDefinitionSearch,),
        }

    attribute_map = {
        "compute": "compute",
        "group_by": "group_by",
        "index": "index",
        "multi_compute": "multi_compute",
        "search": "search",
    }

    def __init__(
        self_,
        compute: Union[LogsQueryCompute, UnsetType] = unset,
        group_by: Union[List[LogQueryDefinitionGroupBy], UnsetType] = unset,
        index: Union[str, UnsetType] = unset,
        multi_compute: Union[List[LogsQueryCompute], UnsetType] = unset,
        search: Union[LogQueryDefinitionSearch, UnsetType] = unset,
        **kwargs,
    ):
        """
        The log query.

        :param compute: Define computation for a log query.
        :type compute: LogsQueryCompute, optional

        :param group_by: List of tag prefixes to group by in the case of a cluster check.
        :type group_by: [LogQueryDefinitionGroupBy], optional

        :param index: A coma separated-list of index names. Use "*" query all indexes at once. `Multiple Indexes <https://docs.datadoghq.com/logs/indexes/#multiple-indexes>`_
        :type index: str, optional

        :param multi_compute: This field is mutually exclusive with ``compute``.
        :type multi_compute: [LogsQueryCompute], optional

        :param search: The query being made on the logs.
        :type search: LogQueryDefinitionSearch, optional
        """
        if compute is not unset:
            kwargs["compute"] = compute
        if group_by is not unset:
            kwargs["group_by"] = group_by
        if index is not unset:
            kwargs["index"] = index
        if multi_compute is not unset:
            kwargs["multi_compute"] = multi_compute
        if search is not unset:
            kwargs["search"] = search
        super().__init__(kwargs)
