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
    from datadog_api_client.v1.model.widget_sort import WidgetSort


class LogQueryDefinitionGroupBySort(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.widget_sort import WidgetSort

        return {
            "aggregation": (str,),
            "facet": (str,),
            "order": (WidgetSort,),
        }

    attribute_map = {
        "aggregation": "aggregation",
        "facet": "facet",
        "order": "order",
    }

    def __init__(self_, aggregation: str, order: WidgetSort, facet: Union[str, UnsetType] = unset, **kwargs):
        """
        Define a sorting method.

        :param aggregation: The aggregation method.
        :type aggregation: str

        :param facet: Facet name.
        :type facet: str, optional

        :param order: Widget sorting methods.
        :type order: WidgetSort
        """
        if facet is not unset:
            kwargs["facet"] = facet
        super().__init__(kwargs)

        self_.aggregation = aggregation
        self_.order = order
