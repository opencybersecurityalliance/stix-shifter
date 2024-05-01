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
    from datadog_api_client.v1.model.log_query_definition_group_by_sort import LogQueryDefinitionGroupBySort


class LogQueryDefinitionGroupBy(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.log_query_definition_group_by_sort import LogQueryDefinitionGroupBySort

        return {
            "facet": (str,),
            "limit": (int,),
            "sort": (LogQueryDefinitionGroupBySort,),
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
        sort: Union[LogQueryDefinitionGroupBySort, UnsetType] = unset,
        **kwargs,
    ):
        """
        Defined items in the group.

        :param facet: Facet name.
        :type facet: str

        :param limit: Maximum number of items in the group.
        :type limit: int, optional

        :param sort: Define a sorting method.
        :type sort: LogQueryDefinitionGroupBySort, optional
        """
        if limit is not unset:
            kwargs["limit"] = limit
        if sort is not unset:
            kwargs["sort"] = sort
        super().__init__(kwargs)

        self_.facet = facet
