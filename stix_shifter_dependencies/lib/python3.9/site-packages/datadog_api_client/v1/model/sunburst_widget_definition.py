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
    from datadog_api_client.v1.model.sunburst_widget_legend import SunburstWidgetLegend
    from datadog_api_client.v1.model.sunburst_widget_request import SunburstWidgetRequest
    from datadog_api_client.v1.model.widget_time import WidgetTime
    from datadog_api_client.v1.model.widget_text_align import WidgetTextAlign
    from datadog_api_client.v1.model.sunburst_widget_definition_type import SunburstWidgetDefinitionType
    from datadog_api_client.v1.model.sunburst_widget_legend_table import SunburstWidgetLegendTable
    from datadog_api_client.v1.model.sunburst_widget_legend_inline_automatic import SunburstWidgetLegendInlineAutomatic


class SunburstWidgetDefinition(ModelNormal):
    validations = {
        "requests": {
            "min_items": 1,
        },
    }

    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.widget_custom_link import WidgetCustomLink
        from datadog_api_client.v1.model.sunburst_widget_legend import SunburstWidgetLegend
        from datadog_api_client.v1.model.sunburst_widget_request import SunburstWidgetRequest
        from datadog_api_client.v1.model.widget_time import WidgetTime
        from datadog_api_client.v1.model.widget_text_align import WidgetTextAlign
        from datadog_api_client.v1.model.sunburst_widget_definition_type import SunburstWidgetDefinitionType

        return {
            "custom_links": ([WidgetCustomLink],),
            "hide_total": (bool,),
            "legend": (SunburstWidgetLegend,),
            "requests": ([SunburstWidgetRequest],),
            "time": (WidgetTime,),
            "title": (str,),
            "title_align": (WidgetTextAlign,),
            "title_size": (str,),
            "type": (SunburstWidgetDefinitionType,),
        }

    attribute_map = {
        "custom_links": "custom_links",
        "hide_total": "hide_total",
        "legend": "legend",
        "requests": "requests",
        "time": "time",
        "title": "title",
        "title_align": "title_align",
        "title_size": "title_size",
        "type": "type",
    }

    def __init__(
        self_,
        requests: List[SunburstWidgetRequest],
        type: SunburstWidgetDefinitionType,
        custom_links: Union[List[WidgetCustomLink], UnsetType] = unset,
        hide_total: Union[bool, UnsetType] = unset,
        legend: Union[
            SunburstWidgetLegend, SunburstWidgetLegendTable, SunburstWidgetLegendInlineAutomatic, UnsetType
        ] = unset,
        time: Union[WidgetTime, UnsetType] = unset,
        title: Union[str, UnsetType] = unset,
        title_align: Union[WidgetTextAlign, UnsetType] = unset,
        title_size: Union[str, UnsetType] = unset,
        **kwargs,
    ):
        """
        Sunbursts are spot on to highlight how groups contribute to the total of a query.

        :param custom_links: List of custom links.
        :type custom_links: [WidgetCustomLink], optional

        :param hide_total: Show the total value in this widget.
        :type hide_total: bool, optional

        :param legend: Configuration of the legend.
        :type legend: SunburstWidgetLegend, optional

        :param requests: List of sunburst widget requests.
        :type requests: [SunburstWidgetRequest]

        :param time: Time setting for the widget.
        :type time: WidgetTime, optional

        :param title: Title of your widget.
        :type title: str, optional

        :param title_align: How to align the text on the widget.
        :type title_align: WidgetTextAlign, optional

        :param title_size: Size of the title.
        :type title_size: str, optional

        :param type: Type of the Sunburst widget.
        :type type: SunburstWidgetDefinitionType
        """
        if custom_links is not unset:
            kwargs["custom_links"] = custom_links
        if hide_total is not unset:
            kwargs["hide_total"] = hide_total
        if legend is not unset:
            kwargs["legend"] = legend
        if time is not unset:
            kwargs["time"] = time
        if title is not unset:
            kwargs["title"] = title
        if title_align is not unset:
            kwargs["title_align"] = title_align
        if title_size is not unset:
            kwargs["title_size"] = title_size
        super().__init__(kwargs)

        self_.requests = requests
        self_.type = type
