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
    from datadog_api_client.v1.model.widget_grouping import WidgetGrouping
    from datadog_api_client.v1.model.widget_time import WidgetTime
    from datadog_api_client.v1.model.widget_text_align import WidgetTextAlign
    from datadog_api_client.v1.model.check_status_widget_definition_type import CheckStatusWidgetDefinitionType


class CheckStatusWidgetDefinition(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.widget_grouping import WidgetGrouping
        from datadog_api_client.v1.model.widget_time import WidgetTime
        from datadog_api_client.v1.model.widget_text_align import WidgetTextAlign
        from datadog_api_client.v1.model.check_status_widget_definition_type import CheckStatusWidgetDefinitionType

        return {
            "check": (str,),
            "group": (str,),
            "group_by": ([str],),
            "grouping": (WidgetGrouping,),
            "tags": ([str],),
            "time": (WidgetTime,),
            "title": (str,),
            "title_align": (WidgetTextAlign,),
            "title_size": (str,),
            "type": (CheckStatusWidgetDefinitionType,),
        }

    attribute_map = {
        "check": "check",
        "group": "group",
        "group_by": "group_by",
        "grouping": "grouping",
        "tags": "tags",
        "time": "time",
        "title": "title",
        "title_align": "title_align",
        "title_size": "title_size",
        "type": "type",
    }

    def __init__(
        self_,
        check: str,
        grouping: WidgetGrouping,
        type: CheckStatusWidgetDefinitionType,
        group: Union[str, UnsetType] = unset,
        group_by: Union[List[str], UnsetType] = unset,
        tags: Union[List[str], UnsetType] = unset,
        time: Union[WidgetTime, UnsetType] = unset,
        title: Union[str, UnsetType] = unset,
        title_align: Union[WidgetTextAlign, UnsetType] = unset,
        title_size: Union[str, UnsetType] = unset,
        **kwargs,
    ):
        """
        Check status shows the current status or number of results for any check performed.

        :param check: Name of the check to use in the widget.
        :type check: str

        :param group: Group reporting a single check.
        :type group: str, optional

        :param group_by: List of tag prefixes to group by in the case of a cluster check.
        :type group_by: [str], optional

        :param grouping: The kind of grouping to use.
        :type grouping: WidgetGrouping

        :param tags: List of tags used to filter the groups reporting a cluster check.
        :type tags: [str], optional

        :param time: Time setting for the widget.
        :type time: WidgetTime, optional

        :param title: Title of the widget.
        :type title: str, optional

        :param title_align: How to align the text on the widget.
        :type title_align: WidgetTextAlign, optional

        :param title_size: Size of the title.
        :type title_size: str, optional

        :param type: Type of the check status widget.
        :type type: CheckStatusWidgetDefinitionType
        """
        if group is not unset:
            kwargs["group"] = group
        if group_by is not unset:
            kwargs["group_by"] = group_by
        if tags is not unset:
            kwargs["tags"] = tags
        if time is not unset:
            kwargs["time"] = time
        if title is not unset:
            kwargs["title"] = title
        if title_align is not unset:
            kwargs["title_align"] = title_align
        if title_size is not unset:
            kwargs["title_size"] = title_size
        super().__init__(kwargs)

        self_.check = check
        self_.grouping = grouping
        self_.type = type
