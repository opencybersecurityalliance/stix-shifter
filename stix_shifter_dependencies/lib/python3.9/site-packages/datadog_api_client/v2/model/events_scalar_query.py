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
    from datadog_api_client.v2.model.events_compute import EventsCompute
    from datadog_api_client.v2.model.events_data_source import EventsDataSource
    from datadog_api_client.v2.model.events_query_group_bys import EventsQueryGroupBys
    from datadog_api_client.v2.model.events_search import EventsSearch


class EventsScalarQuery(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.events_compute import EventsCompute
        from datadog_api_client.v2.model.events_data_source import EventsDataSource
        from datadog_api_client.v2.model.events_query_group_bys import EventsQueryGroupBys
        from datadog_api_client.v2.model.events_search import EventsSearch

        return {
            "compute": (EventsCompute,),
            "data_source": (EventsDataSource,),
            "group_by": (EventsQueryGroupBys,),
            "indexes": ([str],),
            "name": (str,),
            "search": (EventsSearch,),
        }

    attribute_map = {
        "compute": "compute",
        "data_source": "data_source",
        "group_by": "group_by",
        "indexes": "indexes",
        "name": "name",
        "search": "search",
    }

    def __init__(
        self_,
        compute: EventsCompute,
        data_source: EventsDataSource,
        group_by: Union[EventsQueryGroupBys, UnsetType] = unset,
        indexes: Union[List[str], UnsetType] = unset,
        name: Union[str, UnsetType] = unset,
        search: Union[EventsSearch, UnsetType] = unset,
        **kwargs,
    ):
        """
        An individual scalar events query.

        :param compute: The instructions for what to compute for this query.
        :type compute: EventsCompute

        :param data_source: A data source that is powered by the Events Platform.
        :type data_source: EventsDataSource

        :param group_by: The list of facets on which to split results.
        :type group_by: EventsQueryGroupBys, optional

        :param indexes: The indexes in which to search.
        :type indexes: [str], optional

        :param name: The variable name for use in formulas.
        :type name: str, optional

        :param search: Configuration of the search/filter for an events query.
        :type search: EventsSearch, optional
        """
        if group_by is not unset:
            kwargs["group_by"] = group_by
        if indexes is not unset:
            kwargs["indexes"] = indexes
        if name is not unset:
            kwargs["name"] = name
        if search is not unset:
            kwargs["search"] = search
        super().__init__(kwargs)

        self_.compute = compute
        self_.data_source = data_source
