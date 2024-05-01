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
    from datadog_api_client.v1.model.scatter_plot_widget_definition_requests import ScatterPlotWidgetDefinitionRequests
    from datadog_api_client.v1.model.widget_time import WidgetTime
    from datadog_api_client.v1.model.widget_text_align import WidgetTextAlign
    from datadog_api_client.v1.model.scatter_plot_widget_definition_type import ScatterPlotWidgetDefinitionType
    from datadog_api_client.v1.model.widget_axis import WidgetAxis


class ScatterPlotWidgetDefinition(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.widget_custom_link import WidgetCustomLink
        from datadog_api_client.v1.model.scatter_plot_widget_definition_requests import (
            ScatterPlotWidgetDefinitionRequests,
        )
        from datadog_api_client.v1.model.widget_time import WidgetTime
        from datadog_api_client.v1.model.widget_text_align import WidgetTextAlign
        from datadog_api_client.v1.model.scatter_plot_widget_definition_type import ScatterPlotWidgetDefinitionType
        from datadog_api_client.v1.model.widget_axis import WidgetAxis

        return {
            "color_by_groups": ([str],),
            "custom_links": ([WidgetCustomLink],),
            "requests": (ScatterPlotWidgetDefinitionRequests,),
            "time": (WidgetTime,),
            "title": (str,),
            "title_align": (WidgetTextAlign,),
            "title_size": (str,),
            "type": (ScatterPlotWidgetDefinitionType,),
            "xaxis": (WidgetAxis,),
            "yaxis": (WidgetAxis,),
        }

    attribute_map = {
        "color_by_groups": "color_by_groups",
        "custom_links": "custom_links",
        "requests": "requests",
        "time": "time",
        "title": "title",
        "title_align": "title_align",
        "title_size": "title_size",
        "type": "type",
        "xaxis": "xaxis",
        "yaxis": "yaxis",
    }

    def __init__(
        self_,
        requests: ScatterPlotWidgetDefinitionRequests,
        type: ScatterPlotWidgetDefinitionType,
        color_by_groups: Union[List[str], UnsetType] = unset,
        custom_links: Union[List[WidgetCustomLink], UnsetType] = unset,
        time: Union[WidgetTime, UnsetType] = unset,
        title: Union[str, UnsetType] = unset,
        title_align: Union[WidgetTextAlign, UnsetType] = unset,
        title_size: Union[str, UnsetType] = unset,
        xaxis: Union[WidgetAxis, UnsetType] = unset,
        yaxis: Union[WidgetAxis, UnsetType] = unset,
        **kwargs,
    ):
        """
        The scatter plot visualization allows you to graph a chosen scope over two different metrics with their respective aggregation.

        :param color_by_groups: List of groups used for colors.
        :type color_by_groups: [str], optional

        :param custom_links: List of custom links.
        :type custom_links: [WidgetCustomLink], optional

        :param requests: Widget definition.
        :type requests: ScatterPlotWidgetDefinitionRequests

        :param time: Time setting for the widget.
        :type time: WidgetTime, optional

        :param title: Title of your widget.
        :type title: str, optional

        :param title_align: How to align the text on the widget.
        :type title_align: WidgetTextAlign, optional

        :param title_size: Size of the title.
        :type title_size: str, optional

        :param type: Type of the scatter plot widget.
        :type type: ScatterPlotWidgetDefinitionType

        :param xaxis: Axis controls for the widget.
        :type xaxis: WidgetAxis, optional

        :param yaxis: Axis controls for the widget.
        :type yaxis: WidgetAxis, optional
        """
        if color_by_groups is not unset:
            kwargs["color_by_groups"] = color_by_groups
        if custom_links is not unset:
            kwargs["custom_links"] = custom_links
        if time is not unset:
            kwargs["time"] = time
        if title is not unset:
            kwargs["title"] = title
        if title_align is not unset:
            kwargs["title_align"] = title_align
        if title_size is not unset:
            kwargs["title_size"] = title_size
        if xaxis is not unset:
            kwargs["xaxis"] = xaxis
        if yaxis is not unset:
            kwargs["yaxis"] = yaxis
        super().__init__(kwargs)

        self_.requests = requests
        self_.type = type
