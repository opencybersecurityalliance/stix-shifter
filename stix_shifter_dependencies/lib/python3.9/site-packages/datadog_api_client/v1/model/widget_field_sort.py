# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import TYPE_CHECKING

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
)


if TYPE_CHECKING:
    from datadog_api_client.v1.model.widget_sort import WidgetSort


class WidgetFieldSort(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.widget_sort import WidgetSort

        return {
            "column": (str,),
            "order": (WidgetSort,),
        }

    attribute_map = {
        "column": "column",
        "order": "order",
    }

    def __init__(self_, column: str, order: WidgetSort, **kwargs):
        """
        Which column and order to sort by

        :param column: Facet path for the column
        :type column: str

        :param order: Widget sorting methods.
        :type order: WidgetSort
        """
        super().__init__(kwargs)

        self_.column = column
        self_.order = order
