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
    from datadog_api_client.v1.model.widget_layout_type import WidgetLayoutType
    from datadog_api_client.v1.model.widget_text_align import WidgetTextAlign
    from datadog_api_client.v1.model.group_widget_definition_type import GroupWidgetDefinitionType
    from datadog_api_client.v1.model.widget import Widget


class GroupWidgetDefinition(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.widget_layout_type import WidgetLayoutType
        from datadog_api_client.v1.model.widget_text_align import WidgetTextAlign
        from datadog_api_client.v1.model.group_widget_definition_type import GroupWidgetDefinitionType
        from datadog_api_client.v1.model.widget import Widget

        return {
            "background_color": (str,),
            "banner_img": (str,),
            "layout_type": (WidgetLayoutType,),
            "show_title": (bool,),
            "title": (str,),
            "title_align": (WidgetTextAlign,),
            "type": (GroupWidgetDefinitionType,),
            "widgets": ([Widget],),
        }

    attribute_map = {
        "background_color": "background_color",
        "banner_img": "banner_img",
        "layout_type": "layout_type",
        "show_title": "show_title",
        "title": "title",
        "title_align": "title_align",
        "type": "type",
        "widgets": "widgets",
    }

    def __init__(
        self_,
        layout_type: WidgetLayoutType,
        type: GroupWidgetDefinitionType,
        widgets: List[Widget],
        background_color: Union[str, UnsetType] = unset,
        banner_img: Union[str, UnsetType] = unset,
        show_title: Union[bool, UnsetType] = unset,
        title: Union[str, UnsetType] = unset,
        title_align: Union[WidgetTextAlign, UnsetType] = unset,
        **kwargs,
    ):
        """
        The groups widget allows you to keep similar graphs together on your timeboard. Each group has a custom header, can hold one to many graphs, and is collapsible.

        :param background_color: Background color of the group title.
        :type background_color: str, optional

        :param banner_img: URL of image to display as a banner for the group.
        :type banner_img: str, optional

        :param layout_type: Layout type of the group.
        :type layout_type: WidgetLayoutType

        :param show_title: Whether to show the title or not.
        :type show_title: bool, optional

        :param title: Title of the widget.
        :type title: str, optional

        :param title_align: How to align the text on the widget.
        :type title_align: WidgetTextAlign, optional

        :param type: Type of the group widget.
        :type type: GroupWidgetDefinitionType

        :param widgets: List of widget groups.
        :type widgets: [Widget]
        """
        if background_color is not unset:
            kwargs["background_color"] = background_color
        if banner_img is not unset:
            kwargs["banner_img"] = banner_img
        if show_title is not unset:
            kwargs["show_title"] = show_title
        if title is not unset:
            kwargs["title"] = title
        if title_align is not unset:
            kwargs["title_align"] = title_align
        super().__init__(kwargs)

        self_.layout_type = layout_type
        self_.type = type
        self_.widgets = widgets
