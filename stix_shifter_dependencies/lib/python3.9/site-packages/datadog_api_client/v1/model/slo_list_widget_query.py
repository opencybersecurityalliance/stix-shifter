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
    from datadog_api_client.v1.model.widget_field_sort import WidgetFieldSort


class SLOListWidgetQuery(ModelNormal):
    validations = {
        "limit": {
            "inclusive_maximum": 100,
            "inclusive_minimum": 1,
        },
    }

    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.widget_field_sort import WidgetFieldSort

        return {
            "limit": (int,),
            "query_string": (str,),
            "sort": ([WidgetFieldSort],),
        }

    attribute_map = {
        "limit": "limit",
        "query_string": "query_string",
        "sort": "sort",
    }

    def __init__(
        self_,
        query_string: str,
        limit: Union[int, UnsetType] = unset,
        sort: Union[List[WidgetFieldSort], UnsetType] = unset,
        **kwargs,
    ):
        """
        Updated SLO List widget.

        :param limit: Maximum number of results to display in the table.
        :type limit: int, optional

        :param query_string: Widget query.
        :type query_string: str

        :param sort: Options for sorting results.
        :type sort: [WidgetFieldSort], optional
        """
        if limit is not unset:
            kwargs["limit"] = limit
        if sort is not unset:
            kwargs["sort"] = sort
        super().__init__(kwargs)

        self_.query_string = query_string
