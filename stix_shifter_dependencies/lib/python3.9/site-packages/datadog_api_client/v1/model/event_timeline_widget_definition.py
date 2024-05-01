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
    from datadog_api_client.v1.model.widget_time import WidgetTime
    from datadog_api_client.v1.model.widget_text_align import WidgetTextAlign
    from datadog_api_client.v1.model.event_timeline_widget_definition_type import EventTimelineWidgetDefinitionType


class EventTimelineWidgetDefinition(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.widget_time import WidgetTime
        from datadog_api_client.v1.model.widget_text_align import WidgetTextAlign
        from datadog_api_client.v1.model.event_timeline_widget_definition_type import EventTimelineWidgetDefinitionType

        return {
            "query": (str,),
            "tags_execution": (str,),
            "time": (WidgetTime,),
            "title": (str,),
            "title_align": (WidgetTextAlign,),
            "title_size": (str,),
            "type": (EventTimelineWidgetDefinitionType,),
        }

    attribute_map = {
        "query": "query",
        "tags_execution": "tags_execution",
        "time": "time",
        "title": "title",
        "title_align": "title_align",
        "title_size": "title_size",
        "type": "type",
    }

    def __init__(
        self_,
        query: str,
        type: EventTimelineWidgetDefinitionType,
        tags_execution: Union[str, UnsetType] = unset,
        time: Union[WidgetTime, UnsetType] = unset,
        title: Union[str, UnsetType] = unset,
        title_align: Union[WidgetTextAlign, UnsetType] = unset,
        title_size: Union[str, UnsetType] = unset,
        **kwargs,
    ):
        """
        The event timeline is a widget version of the timeline that appears at the top of the Event Stream view. Only available on FREE layout dashboards.

        :param query: Query to filter the event timeline with.
        :type query: str

        :param tags_execution: The execution method for multi-value filters. Can be either and or or.
        :type tags_execution: str, optional

        :param time: Time setting for the widget.
        :type time: WidgetTime, optional

        :param title: Title of the widget.
        :type title: str, optional

        :param title_align: How to align the text on the widget.
        :type title_align: WidgetTextAlign, optional

        :param title_size: Size of the title.
        :type title_size: str, optional

        :param type: Type of the event timeline widget.
        :type type: EventTimelineWidgetDefinitionType
        """
        if tags_execution is not unset:
            kwargs["tags_execution"] = tags_execution
        if time is not unset:
            kwargs["time"] = time
        if title is not unset:
            kwargs["title"] = title
        if title_align is not unset:
            kwargs["title_align"] = title_align
        if title_size is not unset:
            kwargs["title_size"] = title_size
        super().__init__(kwargs)

        self_.query = query
        self_.type = type
