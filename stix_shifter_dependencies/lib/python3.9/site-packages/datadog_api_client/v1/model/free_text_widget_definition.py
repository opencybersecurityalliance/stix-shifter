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
    from datadog_api_client.v1.model.free_text_widget_definition_type import FreeTextWidgetDefinitionType


class FreeTextWidgetDefinition(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.widget_text_align import WidgetTextAlign
        from datadog_api_client.v1.model.free_text_widget_definition_type import FreeTextWidgetDefinitionType

        return {
            "color": (str,),
            "font_size": (str,),
            "text": (str,),
            "text_align": (WidgetTextAlign,),
            "type": (FreeTextWidgetDefinitionType,),
        }

    attribute_map = {
        "color": "color",
        "font_size": "font_size",
        "text": "text",
        "text_align": "text_align",
        "type": "type",
    }

    def __init__(
        self_,
        text: str,
        type: FreeTextWidgetDefinitionType,
        color: Union[str, UnsetType] = unset,
        font_size: Union[str, UnsetType] = unset,
        text_align: Union[WidgetTextAlign, UnsetType] = unset,
        **kwargs,
    ):
        """
        Free text is a widget that allows you to add headings to your screenboard. Commonly used to state the overall purpose of the dashboard. Only available on FREE layout dashboards.

        :param color: Color of the text.
        :type color: str, optional

        :param font_size: Size of the text.
        :type font_size: str, optional

        :param text: Text to display.
        :type text: str

        :param text_align: How to align the text on the widget.
        :type text_align: WidgetTextAlign, optional

        :param type: Type of the free text widget.
        :type type: FreeTextWidgetDefinitionType
        """
        if color is not unset:
            kwargs["color"] = color
        if font_size is not unset:
            kwargs["font_size"] = font_size
        if text_align is not unset:
            kwargs["text_align"] = text_align
        super().__init__(kwargs)

        self_.text = text
        self_.type = type
