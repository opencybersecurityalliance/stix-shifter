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
    from datadog_api_client.v1.model.widget_text_align import WidgetTextAlign
    from datadog_api_client.v1.model.widget_tick_edge import WidgetTickEdge
    from datadog_api_client.v1.model.note_widget_definition_type import NoteWidgetDefinitionType
    from datadog_api_client.v1.model.widget_vertical_align import WidgetVerticalAlign


class NoteWidgetDefinition(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.widget_text_align import WidgetTextAlign
        from datadog_api_client.v1.model.widget_tick_edge import WidgetTickEdge
        from datadog_api_client.v1.model.note_widget_definition_type import NoteWidgetDefinitionType
        from datadog_api_client.v1.model.widget_vertical_align import WidgetVerticalAlign

        return {
            "background_color": (str,),
            "content": (str,),
            "font_size": (str,),
            "has_padding": (bool,),
            "show_tick": (bool,),
            "text_align": (WidgetTextAlign,),
            "tick_edge": (WidgetTickEdge,),
            "tick_pos": (str,),
            "type": (NoteWidgetDefinitionType,),
            "vertical_align": (WidgetVerticalAlign,),
        }

    attribute_map = {
        "background_color": "background_color",
        "content": "content",
        "font_size": "font_size",
        "has_padding": "has_padding",
        "show_tick": "show_tick",
        "text_align": "text_align",
        "tick_edge": "tick_edge",
        "tick_pos": "tick_pos",
        "type": "type",
        "vertical_align": "vertical_align",
    }

    def __init__(
        self_,
        content: str,
        type: NoteWidgetDefinitionType,
        background_color: Union[str, UnsetType] = unset,
        font_size: Union[str, UnsetType] = unset,
        has_padding: Union[bool, UnsetType] = unset,
        show_tick: Union[bool, UnsetType] = unset,
        text_align: Union[WidgetTextAlign, UnsetType] = unset,
        tick_edge: Union[WidgetTickEdge, UnsetType] = unset,
        tick_pos: Union[str, UnsetType] = unset,
        vertical_align: Union[WidgetVerticalAlign, UnsetType] = unset,
        **kwargs,
    ):
        """
        The notes and links widget is similar to free text widget, but allows for more formatting options.

        :param background_color: Background color of the note.
        :type background_color: str, optional

        :param content: Content of the note.
        :type content: str

        :param font_size: Size of the text.
        :type font_size: str, optional

        :param has_padding: Whether to add padding or not.
        :type has_padding: bool, optional

        :param show_tick: Whether to show a tick or not.
        :type show_tick: bool, optional

        :param text_align: How to align the text on the widget.
        :type text_align: WidgetTextAlign, optional

        :param tick_edge: Define how you want to align the text on the widget.
        :type tick_edge: WidgetTickEdge, optional

        :param tick_pos: Where to position the tick on an edge.
        :type tick_pos: str, optional

        :param type: Type of the note widget.
        :type type: NoteWidgetDefinitionType

        :param vertical_align: Vertical alignment.
        :type vertical_align: WidgetVerticalAlign, optional
        """
        if background_color is not unset:
            kwargs["background_color"] = background_color
        if font_size is not unset:
            kwargs["font_size"] = font_size
        if has_padding is not unset:
            kwargs["has_padding"] = has_padding
        if show_tick is not unset:
            kwargs["show_tick"] = show_tick
        if text_align is not unset:
            kwargs["text_align"] = text_align
        if tick_edge is not unset:
            kwargs["tick_edge"] = tick_edge
        if tick_pos is not unset:
            kwargs["tick_pos"] = tick_pos
        if vertical_align is not unset:
            kwargs["vertical_align"] = vertical_align
        super().__init__(kwargs)

        self_.content = content
        self_.type = type
