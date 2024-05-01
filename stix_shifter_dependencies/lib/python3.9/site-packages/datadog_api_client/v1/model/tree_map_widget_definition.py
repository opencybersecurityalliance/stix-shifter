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
    from datadog_api_client.v1.model.tree_map_color_by import TreeMapColorBy
    from datadog_api_client.v1.model.widget_custom_link import WidgetCustomLink
    from datadog_api_client.v1.model.tree_map_group_by import TreeMapGroupBy
    from datadog_api_client.v1.model.tree_map_widget_request import TreeMapWidgetRequest
    from datadog_api_client.v1.model.tree_map_size_by import TreeMapSizeBy
    from datadog_api_client.v1.model.widget_time import WidgetTime
    from datadog_api_client.v1.model.tree_map_widget_definition_type import TreeMapWidgetDefinitionType


class TreeMapWidgetDefinition(ModelNormal):
    validations = {
        "requests": {
            "max_items": 1,
            "min_items": 1,
        },
    }

    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.tree_map_color_by import TreeMapColorBy
        from datadog_api_client.v1.model.widget_custom_link import WidgetCustomLink
        from datadog_api_client.v1.model.tree_map_group_by import TreeMapGroupBy
        from datadog_api_client.v1.model.tree_map_widget_request import TreeMapWidgetRequest
        from datadog_api_client.v1.model.tree_map_size_by import TreeMapSizeBy
        from datadog_api_client.v1.model.widget_time import WidgetTime
        from datadog_api_client.v1.model.tree_map_widget_definition_type import TreeMapWidgetDefinitionType

        return {
            "color_by": (TreeMapColorBy,),
            "custom_links": ([WidgetCustomLink],),
            "group_by": (TreeMapGroupBy,),
            "requests": ([TreeMapWidgetRequest],),
            "size_by": (TreeMapSizeBy,),
            "time": (WidgetTime,),
            "title": (str,),
            "type": (TreeMapWidgetDefinitionType,),
        }

    attribute_map = {
        "color_by": "color_by",
        "custom_links": "custom_links",
        "group_by": "group_by",
        "requests": "requests",
        "size_by": "size_by",
        "time": "time",
        "title": "title",
        "type": "type",
    }

    def __init__(
        self_,
        requests: List[TreeMapWidgetRequest],
        type: TreeMapWidgetDefinitionType,
        color_by: Union[TreeMapColorBy, UnsetType] = unset,
        custom_links: Union[List[WidgetCustomLink], UnsetType] = unset,
        group_by: Union[TreeMapGroupBy, UnsetType] = unset,
        size_by: Union[TreeMapSizeBy, UnsetType] = unset,
        time: Union[WidgetTime, UnsetType] = unset,
        title: Union[str, UnsetType] = unset,
        **kwargs,
    ):
        """
        The treemap visualization enables you to display hierarchical and nested data. It is well suited for queries that describe part-whole relationships, such as resource usage by availability zone, data center, or team.

        :param color_by: (deprecated) The attribute formerly used to determine color in the widget. **Deprecated**.
        :type color_by: TreeMapColorBy, optional

        :param custom_links: List of custom links.
        :type custom_links: [WidgetCustomLink], optional

        :param group_by: (deprecated) The attribute formerly used to group elements in the widget. **Deprecated**.
        :type group_by: TreeMapGroupBy, optional

        :param requests: List of treemap widget requests.
        :type requests: [TreeMapWidgetRequest]

        :param size_by: (deprecated) The attribute formerly used to determine size in the widget. **Deprecated**.
        :type size_by: TreeMapSizeBy, optional

        :param time: Time setting for the widget.
        :type time: WidgetTime, optional

        :param title: Title of your widget.
        :type title: str, optional

        :param type: Type of the treemap widget.
        :type type: TreeMapWidgetDefinitionType
        """
        if color_by is not unset:
            kwargs["color_by"] = color_by
        if custom_links is not unset:
            kwargs["custom_links"] = custom_links
        if group_by is not unset:
            kwargs["group_by"] = group_by
        if size_by is not unset:
            kwargs["size_by"] = size_by
        if time is not unset:
            kwargs["time"] = time
        if title is not unset:
            kwargs["title"] = title
        super().__init__(kwargs)

        self_.requests = requests
        self_.type = type
