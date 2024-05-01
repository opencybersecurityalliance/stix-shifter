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
    from datadog_api_client.v1.model.widget_color_preference import WidgetColorPreference
    from datadog_api_client.v1.model.widget_monitor_summary_display_format import WidgetMonitorSummaryDisplayFormat
    from datadog_api_client.v1.model.widget_monitor_summary_sort import WidgetMonitorSummarySort
    from datadog_api_client.v1.model.widget_summary_type import WidgetSummaryType
    from datadog_api_client.v1.model.widget_text_align import WidgetTextAlign
    from datadog_api_client.v1.model.monitor_summary_widget_definition_type import MonitorSummaryWidgetDefinitionType


class MonitorSummaryWidgetDefinition(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.widget_color_preference import WidgetColorPreference
        from datadog_api_client.v1.model.widget_monitor_summary_display_format import WidgetMonitorSummaryDisplayFormat
        from datadog_api_client.v1.model.widget_monitor_summary_sort import WidgetMonitorSummarySort
        from datadog_api_client.v1.model.widget_summary_type import WidgetSummaryType
        from datadog_api_client.v1.model.widget_text_align import WidgetTextAlign
        from datadog_api_client.v1.model.monitor_summary_widget_definition_type import (
            MonitorSummaryWidgetDefinitionType,
        )

        return {
            "color_preference": (WidgetColorPreference,),
            "count": (int,),
            "display_format": (WidgetMonitorSummaryDisplayFormat,),
            "hide_zero_counts": (bool,),
            "query": (str,),
            "show_last_triggered": (bool,),
            "show_priority": (bool,),
            "sort": (WidgetMonitorSummarySort,),
            "start": (int,),
            "summary_type": (WidgetSummaryType,),
            "title": (str,),
            "title_align": (WidgetTextAlign,),
            "title_size": (str,),
            "type": (MonitorSummaryWidgetDefinitionType,),
        }

    attribute_map = {
        "color_preference": "color_preference",
        "count": "count",
        "display_format": "display_format",
        "hide_zero_counts": "hide_zero_counts",
        "query": "query",
        "show_last_triggered": "show_last_triggered",
        "show_priority": "show_priority",
        "sort": "sort",
        "start": "start",
        "summary_type": "summary_type",
        "title": "title",
        "title_align": "title_align",
        "title_size": "title_size",
        "type": "type",
    }

    def __init__(
        self_,
        query: str,
        type: MonitorSummaryWidgetDefinitionType,
        color_preference: Union[WidgetColorPreference, UnsetType] = unset,
        count: Union[int, UnsetType] = unset,
        display_format: Union[WidgetMonitorSummaryDisplayFormat, UnsetType] = unset,
        hide_zero_counts: Union[bool, UnsetType] = unset,
        show_last_triggered: Union[bool, UnsetType] = unset,
        show_priority: Union[bool, UnsetType] = unset,
        sort: Union[WidgetMonitorSummarySort, UnsetType] = unset,
        start: Union[int, UnsetType] = unset,
        summary_type: Union[WidgetSummaryType, UnsetType] = unset,
        title: Union[str, UnsetType] = unset,
        title_align: Union[WidgetTextAlign, UnsetType] = unset,
        title_size: Union[str, UnsetType] = unset,
        **kwargs,
    ):
        """
        The monitor summary widget displays a summary view of all your Datadog monitors, or a subset based on a query. Only available on FREE layout dashboards.

        :param color_preference: Which color to use on the widget.
        :type color_preference: WidgetColorPreference, optional

        :param count: The number of monitors to display. **Deprecated**.
        :type count: int, optional

        :param display_format: What to display on the widget.
        :type display_format: WidgetMonitorSummaryDisplayFormat, optional

        :param hide_zero_counts: Whether to show counts of 0 or not.
        :type hide_zero_counts: bool, optional

        :param query: Query to filter the monitors with.
        :type query: str

        :param show_last_triggered: Whether to show the time that has elapsed since the monitor/group triggered.
        :type show_last_triggered: bool, optional

        :param show_priority: Whether to show the priorities column.
        :type show_priority: bool, optional

        :param sort: Widget sorting methods.
        :type sort: WidgetMonitorSummarySort, optional

        :param start: The start of the list. Typically 0. **Deprecated**.
        :type start: int, optional

        :param summary_type: Which summary type should be used.
        :type summary_type: WidgetSummaryType, optional

        :param title: Title of the widget.
        :type title: str, optional

        :param title_align: How to align the text on the widget.
        :type title_align: WidgetTextAlign, optional

        :param title_size: Size of the title.
        :type title_size: str, optional

        :param type: Type of the monitor summary widget.
        :type type: MonitorSummaryWidgetDefinitionType
        """
        if color_preference is not unset:
            kwargs["color_preference"] = color_preference
        if count is not unset:
            kwargs["count"] = count
        if display_format is not unset:
            kwargs["display_format"] = display_format
        if hide_zero_counts is not unset:
            kwargs["hide_zero_counts"] = hide_zero_counts
        if show_last_triggered is not unset:
            kwargs["show_last_triggered"] = show_last_triggered
        if show_priority is not unset:
            kwargs["show_priority"] = show_priority
        if sort is not unset:
            kwargs["sort"] = sort
        if start is not unset:
            kwargs["start"] = start
        if summary_type is not unset:
            kwargs["summary_type"] = summary_type
        if title is not unset:
            kwargs["title"] = title
        if title_align is not unset:
            kwargs["title_align"] = title_align
        if title_size is not unset:
            kwargs["title_size"] = title_size
        super().__init__(kwargs)

        self_.query = query
        self_.type = type
