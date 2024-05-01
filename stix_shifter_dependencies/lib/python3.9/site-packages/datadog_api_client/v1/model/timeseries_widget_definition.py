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
    from datadog_api_client.v1.model.widget_event import WidgetEvent
    from datadog_api_client.v1.model.timeseries_widget_legend_column import TimeseriesWidgetLegendColumn
    from datadog_api_client.v1.model.timeseries_widget_legend_layout import TimeseriesWidgetLegendLayout
    from datadog_api_client.v1.model.widget_marker import WidgetMarker
    from datadog_api_client.v1.model.timeseries_widget_request import TimeseriesWidgetRequest
    from datadog_api_client.v1.model.widget_axis import WidgetAxis
    from datadog_api_client.v1.model.widget_time import WidgetTime
    from datadog_api_client.v1.model.widget_text_align import WidgetTextAlign
    from datadog_api_client.v1.model.timeseries_widget_definition_type import TimeseriesWidgetDefinitionType


class TimeseriesWidgetDefinition(ModelNormal):
    validations = {
        "requests": {
            "min_items": 1,
        },
    }

    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.widget_custom_link import WidgetCustomLink
        from datadog_api_client.v1.model.widget_event import WidgetEvent
        from datadog_api_client.v1.model.timeseries_widget_legend_column import TimeseriesWidgetLegendColumn
        from datadog_api_client.v1.model.timeseries_widget_legend_layout import TimeseriesWidgetLegendLayout
        from datadog_api_client.v1.model.widget_marker import WidgetMarker
        from datadog_api_client.v1.model.timeseries_widget_request import TimeseriesWidgetRequest
        from datadog_api_client.v1.model.widget_axis import WidgetAxis
        from datadog_api_client.v1.model.widget_time import WidgetTime
        from datadog_api_client.v1.model.widget_text_align import WidgetTextAlign
        from datadog_api_client.v1.model.timeseries_widget_definition_type import TimeseriesWidgetDefinitionType

        return {
            "custom_links": ([WidgetCustomLink],),
            "events": ([WidgetEvent],),
            "legend_columns": ([TimeseriesWidgetLegendColumn],),
            "legend_layout": (TimeseriesWidgetLegendLayout,),
            "legend_size": (str,),
            "markers": ([WidgetMarker],),
            "requests": ([TimeseriesWidgetRequest],),
            "right_yaxis": (WidgetAxis,),
            "show_legend": (bool,),
            "time": (WidgetTime,),
            "title": (str,),
            "title_align": (WidgetTextAlign,),
            "title_size": (str,),
            "type": (TimeseriesWidgetDefinitionType,),
            "yaxis": (WidgetAxis,),
        }

    attribute_map = {
        "custom_links": "custom_links",
        "events": "events",
        "legend_columns": "legend_columns",
        "legend_layout": "legend_layout",
        "legend_size": "legend_size",
        "markers": "markers",
        "requests": "requests",
        "right_yaxis": "right_yaxis",
        "show_legend": "show_legend",
        "time": "time",
        "title": "title",
        "title_align": "title_align",
        "title_size": "title_size",
        "type": "type",
        "yaxis": "yaxis",
    }

    def __init__(
        self_,
        requests: List[TimeseriesWidgetRequest],
        type: TimeseriesWidgetDefinitionType,
        custom_links: Union[List[WidgetCustomLink], UnsetType] = unset,
        events: Union[List[WidgetEvent], UnsetType] = unset,
        legend_columns: Union[List[TimeseriesWidgetLegendColumn], UnsetType] = unset,
        legend_layout: Union[TimeseriesWidgetLegendLayout, UnsetType] = unset,
        legend_size: Union[str, UnsetType] = unset,
        markers: Union[List[WidgetMarker], UnsetType] = unset,
        right_yaxis: Union[WidgetAxis, UnsetType] = unset,
        show_legend: Union[bool, UnsetType] = unset,
        time: Union[WidgetTime, UnsetType] = unset,
        title: Union[str, UnsetType] = unset,
        title_align: Union[WidgetTextAlign, UnsetType] = unset,
        title_size: Union[str, UnsetType] = unset,
        yaxis: Union[WidgetAxis, UnsetType] = unset,
        **kwargs,
    ):
        """
        The timeseries visualization allows you to display the evolution of one or more metrics, log events, or Indexed Spans over time.

        :param custom_links: List of custom links.
        :type custom_links: [WidgetCustomLink], optional

        :param events: List of widget events.
        :type events: [WidgetEvent], optional

        :param legend_columns: Columns displayed in the legend.
        :type legend_columns: [TimeseriesWidgetLegendColumn], optional

        :param legend_layout: Layout of the legend.
        :type legend_layout: TimeseriesWidgetLegendLayout, optional

        :param legend_size: Available legend sizes for a widget. Should be one of "0", "2", "4", "8", "16", or "auto".
        :type legend_size: str, optional

        :param markers: List of markers.
        :type markers: [WidgetMarker], optional

        :param requests: List of timeseries widget requests.
        :type requests: [TimeseriesWidgetRequest]

        :param right_yaxis: Axis controls for the widget.
        :type right_yaxis: WidgetAxis, optional

        :param show_legend: (screenboard only) Show the legend for this widget.
        :type show_legend: bool, optional

        :param time: Time setting for the widget.
        :type time: WidgetTime, optional

        :param title: Title of your widget.
        :type title: str, optional

        :param title_align: How to align the text on the widget.
        :type title_align: WidgetTextAlign, optional

        :param title_size: Size of the title.
        :type title_size: str, optional

        :param type: Type of the timeseries widget.
        :type type: TimeseriesWidgetDefinitionType

        :param yaxis: Axis controls for the widget.
        :type yaxis: WidgetAxis, optional
        """
        if custom_links is not unset:
            kwargs["custom_links"] = custom_links
        if events is not unset:
            kwargs["events"] = events
        if legend_columns is not unset:
            kwargs["legend_columns"] = legend_columns
        if legend_layout is not unset:
            kwargs["legend_layout"] = legend_layout
        if legend_size is not unset:
            kwargs["legend_size"] = legend_size
        if markers is not unset:
            kwargs["markers"] = markers
        if right_yaxis is not unset:
            kwargs["right_yaxis"] = right_yaxis
        if show_legend is not unset:
            kwargs["show_legend"] = show_legend
        if time is not unset:
            kwargs["time"] = time
        if title is not unset:
            kwargs["title"] = title
        if title_align is not unset:
            kwargs["title_align"] = title_align
        if title_size is not unset:
            kwargs["title_size"] = title_size
        if yaxis is not unset:
            kwargs["yaxis"] = yaxis
        super().__init__(kwargs)

        self_.requests = requests
        self_.type = type
