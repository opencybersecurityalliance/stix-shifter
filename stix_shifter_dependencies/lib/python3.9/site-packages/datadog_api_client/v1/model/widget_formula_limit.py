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
    from datadog_api_client.v1.model.query_sort_order import QuerySortOrder


class WidgetFormulaLimit(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.query_sort_order import QuerySortOrder

        return {
            "count": (int,),
            "order": (QuerySortOrder,),
        }

    attribute_map = {
        "count": "count",
        "order": "order",
    }

    def __init__(
        self_, count: Union[int, UnsetType] = unset, order: Union[QuerySortOrder, UnsetType] = unset, **kwargs
    ):
        """
        Options for limiting results returned.

        :param count: Number of results to return.
        :type count: int, optional

        :param order: Direction of sort.
        :type order: QuerySortOrder, optional
        """
        if count is not unset:
            kwargs["count"] = count
        if order is not unset:
            kwargs["order"] = order
        super().__init__(kwargs)
