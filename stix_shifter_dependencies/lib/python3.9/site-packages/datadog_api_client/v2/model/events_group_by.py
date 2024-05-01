# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Union, TYPE_CHECKING

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    unset,
    UnsetType,
)


if TYPE_CHECKING:
    from datadog_api_client.v2.model.events_group_by_sort import EventsGroupBySort


class EventsGroupBy(ModelNormal):
    validations = {
        "limit": {
            "inclusive_maximum": 2147483647,
        },
    }

    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.events_group_by_sort import EventsGroupBySort

        return {
            "facet": (str,),
            "limit": (int,),
            "sort": (EventsGroupBySort,),
        }

    attribute_map = {
        "facet": "facet",
        "limit": "limit",
        "sort": "sort",
    }

    def __init__(
        self_,
        facet: str,
        limit: Union[int, UnsetType] = unset,
        sort: Union[EventsGroupBySort, UnsetType] = unset,
        **kwargs,
    ):
        """
        A dimension on which to split a query's results.

        :param facet: The facet by which to split groups.
        :type facet: str

        :param limit: The maximum number of groups to return.
        :type limit: int, optional

        :param sort: The dimension by which to sort a query's results.
        :type sort: EventsGroupBySort, optional
        """
        if limit is not unset:
            kwargs["limit"] = limit
        if sort is not unset:
            kwargs["sort"] = sort
        super().__init__(kwargs)

        self_.facet = facet
