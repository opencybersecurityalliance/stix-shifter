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
    from datadog_api_client.v1.model.widget_custom_link import WidgetCustomLink
    from datadog_api_client.v1.model.query_value_widget_request import QueryValueWidgetRequest
    from datadog_api_client.v1.model.widget_text_align import WidgetTextAlign
    from datadog_api_client.v1.model.widget_time import WidgetTime
    from datadog_api_client.v1.model.timeseries_background import TimeseriesBackground
    from datadog_api_client.v1.model.query_value_widget_definition_type import QueryValueWidgetDefinitionType


class QueryValueWidgetDefinition(ModelNormal):
    validations = {
        "requests": {
            "max_items": 1,
            "min_items": 1,
        },
    }

    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.widget_custom_link import WidgetCustomLink
        from datadog_api_client.v1.model.query_value_widget_request import QueryValueWidgetRequest
        from datadog_api_client.v1.model.widget_text_align import WidgetTextAlign
        from datadog_api_client.v1.model.widget_time import WidgetTime
        from datadog_api_client.v1.model.timeseries_background import TimeseriesBackground
        from datadog_api_client.v1.model.query_value_widget_definition_type import QueryValueWidgetDefinitionType

        return {
            "autoscale": (bool,),
            "custom_links": ([WidgetCustomLink],),
            "custom_unit": (str,),
            "precision": (int,),
            "requests": ([QueryValueWidgetRequest],),
            "text_align": (WidgetTextAlign,),
            "time": (WidgetTime,),
            "timeseries_background": (TimeseriesBackground,),
            "title": (str,),
            "title_align": (WidgetTextAlign,),
            "title_size": (str,),
            "type": (QueryValueWidgetDefinitionType,),
        }

    attribute_map = {
        "autoscale": "autoscale",
        "custom_links": "custom_links",
        "custom_unit": "custom_unit",
        "precision": "precision",
        "requests": "requests",
        "text_align": "text_align",
        "time": "time",
        "timeseries_background": "timeseries_background",
        "title": "title",
        "title_align": "title_align",
        "title_size": "title_size",
        "type": "type",
    }

    def __init__(
        self_,
        requests: List[QueryValueWidgetRequest],
        type: QueryValueWidgetDefinitionType,
        autoscale: Union[bool, UnsetType] = unset,
        custom_links: Union[List[WidgetCustomLink], UnsetType] = unset,
        custom_unit: Union[str, UnsetType] = unset,
        precision: Union[int, UnsetType] = unset,
        text_align: Union[WidgetTextAlign, UnsetType] = unset,
        time: Union[WidgetTime, UnsetType] = unset,
        timeseries_background: Union[TimeseriesBackground, UnsetType] = unset,
        title: Union[str, UnsetType] = unset,
        title_align: Union[WidgetTextAlign, UnsetType] = unset,
        title_size: Union[str, UnsetType] = unset,
        **kwargs,
    ):
        """
        Query values display the current value of a given metric, APM, or log query.

        :param autoscale: Whether to use auto-scaling or not.
        :type autoscale: bool, optional

        :param custom_links: List of custom links.
        :type custom_links: [WidgetCustomLink], optional

        :param custom_unit: Display a unit of your choice on the widget.
        :type custom_unit: str, optional

        :param precision: Number of decimals to show. If not defined, the widget uses the raw value.
        :type precision: int, optional

        :param requests: Widget definition.
        :type requests: [QueryValueWidgetRequest]

        :param text_align: How to align the text on the widget.
        :type text_align: WidgetTextAlign, optional

        :param time: Time setting for the widget.
        :type time: WidgetTime, optional

        :param timeseries_background: Set a timeseries on the widget background.
        :type timeseries_background: TimeseriesBackground, optional

        :param title: Title of your widget.
        :type title: str, optional

        :param title_align: How to align the text on the widget.
        :type title_align: WidgetTextAlign, optional

        :param title_size: Size of the title.
        :type title_size: str, optional

        :param type: Type of the query value widget.
        :type type: QueryValueWidgetDefinitionType
        """
        if autoscale is not unset:
            kwargs["autoscale"] = autoscale
        if custom_links is not unset:
            kwargs["custom_links"] = custom_links
        if custom_unit is not unset:
            kwargs["custom_unit"] = custom_unit
        if precision is not unset:
            kwargs["precision"] = precision
        if text_align is not unset:
            kwargs["text_align"] = text_align
        if time is not unset:
            kwargs["time"] = time
        if timeseries_background is not unset:
            kwargs["timeseries_background"] = timeseries_background
        if title is not unset:
            kwargs["title"] = title
        if title_align is not unset:
            kwargs["title_align"] = title_align
        if title_size is not unset:
            kwargs["title_size"] = title_size
        super().__init__(kwargs)

        self_.requests = requests
        self_.type = type
