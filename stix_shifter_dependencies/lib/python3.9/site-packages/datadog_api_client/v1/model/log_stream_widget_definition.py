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
    from datadog_api_client.v1.model.widget_message_display import WidgetMessageDisplay
    from datadog_api_client.v1.model.widget_field_sort import WidgetFieldSort
    from datadog_api_client.v1.model.widget_time import WidgetTime
    from datadog_api_client.v1.model.widget_text_align import WidgetTextAlign
    from datadog_api_client.v1.model.log_stream_widget_definition_type import LogStreamWidgetDefinitionType


class LogStreamWidgetDefinition(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.widget_message_display import WidgetMessageDisplay
        from datadog_api_client.v1.model.widget_field_sort import WidgetFieldSort
        from datadog_api_client.v1.model.widget_time import WidgetTime
        from datadog_api_client.v1.model.widget_text_align import WidgetTextAlign
        from datadog_api_client.v1.model.log_stream_widget_definition_type import LogStreamWidgetDefinitionType

        return {
            "columns": ([str],),
            "indexes": ([str],),
            "logset": (str,),
            "message_display": (WidgetMessageDisplay,),
            "query": (str,),
            "show_date_column": (bool,),
            "show_message_column": (bool,),
            "sort": (WidgetFieldSort,),
            "time": (WidgetTime,),
            "title": (str,),
            "title_align": (WidgetTextAlign,),
            "title_size": (str,),
            "type": (LogStreamWidgetDefinitionType,),
        }

    attribute_map = {
        "columns": "columns",
        "indexes": "indexes",
        "logset": "logset",
        "message_display": "message_display",
        "query": "query",
        "show_date_column": "show_date_column",
        "show_message_column": "show_message_column",
        "sort": "sort",
        "time": "time",
        "title": "title",
        "title_align": "title_align",
        "title_size": "title_size",
        "type": "type",
    }

    def __init__(
        self_,
        type: LogStreamWidgetDefinitionType,
        columns: Union[List[str], UnsetType] = unset,
        indexes: Union[List[str], UnsetType] = unset,
        logset: Union[str, UnsetType] = unset,
        message_display: Union[WidgetMessageDisplay, UnsetType] = unset,
        query: Union[str, UnsetType] = unset,
        show_date_column: Union[bool, UnsetType] = unset,
        show_message_column: Union[bool, UnsetType] = unset,
        sort: Union[WidgetFieldSort, UnsetType] = unset,
        time: Union[WidgetTime, UnsetType] = unset,
        title: Union[str, UnsetType] = unset,
        title_align: Union[WidgetTextAlign, UnsetType] = unset,
        title_size: Union[str, UnsetType] = unset,
        **kwargs,
    ):
        """
        The Log Stream displays a log flow matching the defined query. Only available on FREE layout dashboards.

        :param columns: Which columns to display on the widget.
        :type columns: [str], optional

        :param indexes: An array of index names to query in the stream. Use [] to query all indexes at once.
        :type indexes: [str], optional

        :param logset: ID of the log set to use. **Deprecated**.
        :type logset: str, optional

        :param message_display: Amount of log lines to display
        :type message_display: WidgetMessageDisplay, optional

        :param query: Query to filter the log stream with.
        :type query: str, optional

        :param show_date_column: Whether to show the date column or not
        :type show_date_column: bool, optional

        :param show_message_column: Whether to show the message column or not
        :type show_message_column: bool, optional

        :param sort: Which column and order to sort by
        :type sort: WidgetFieldSort, optional

        :param time: Time setting for the widget.
        :type time: WidgetTime, optional

        :param title: Title of the widget.
        :type title: str, optional

        :param title_align: How to align the text on the widget.
        :type title_align: WidgetTextAlign, optional

        :param title_size: Size of the title.
        :type title_size: str, optional

        :param type: Type of the log stream widget.
        :type type: LogStreamWidgetDefinitionType
        """
        if columns is not unset:
            kwargs["columns"] = columns
        if indexes is not unset:
            kwargs["indexes"] = indexes
        if logset is not unset:
            kwargs["logset"] = logset
        if message_display is not unset:
            kwargs["message_display"] = message_display
        if query is not unset:
            kwargs["query"] = query
        if show_date_column is not unset:
            kwargs["show_date_column"] = show_date_column
        if show_message_column is not unset:
            kwargs["show_message_column"] = show_message_column
        if sort is not unset:
            kwargs["sort"] = sort
        if time is not unset:
            kwargs["time"] = time
        if title is not unset:
            kwargs["title"] = title
        if title_align is not unset:
            kwargs["title_align"] = title_align
        if title_size is not unset:
            kwargs["title_size"] = title_size
        super().__init__(kwargs)

        self_.type = type
