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
    from datadog_api_client.v1.model.widget_node_type import WidgetNodeType
    from datadog_api_client.v1.model.host_map_widget_definition_requests import HostMapWidgetDefinitionRequests
    from datadog_api_client.v1.model.host_map_widget_definition_style import HostMapWidgetDefinitionStyle
    from datadog_api_client.v1.model.widget_text_align import WidgetTextAlign
    from datadog_api_client.v1.model.host_map_widget_definition_type import HostMapWidgetDefinitionType


class HostMapWidgetDefinition(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.widget_custom_link import WidgetCustomLink
        from datadog_api_client.v1.model.widget_node_type import WidgetNodeType
        from datadog_api_client.v1.model.host_map_widget_definition_requests import HostMapWidgetDefinitionRequests
        from datadog_api_client.v1.model.host_map_widget_definition_style import HostMapWidgetDefinitionStyle
        from datadog_api_client.v1.model.widget_text_align import WidgetTextAlign
        from datadog_api_client.v1.model.host_map_widget_definition_type import HostMapWidgetDefinitionType

        return {
            "custom_links": ([WidgetCustomLink],),
            "group": ([str],),
            "no_group_hosts": (bool,),
            "no_metric_hosts": (bool,),
            "node_type": (WidgetNodeType,),
            "notes": (str,),
            "requests": (HostMapWidgetDefinitionRequests,),
            "scope": ([str],),
            "style": (HostMapWidgetDefinitionStyle,),
            "title": (str,),
            "title_align": (WidgetTextAlign,),
            "title_size": (str,),
            "type": (HostMapWidgetDefinitionType,),
        }

    attribute_map = {
        "custom_links": "custom_links",
        "group": "group",
        "no_group_hosts": "no_group_hosts",
        "no_metric_hosts": "no_metric_hosts",
        "node_type": "node_type",
        "notes": "notes",
        "requests": "requests",
        "scope": "scope",
        "style": "style",
        "title": "title",
        "title_align": "title_align",
        "title_size": "title_size",
        "type": "type",
    }

    def __init__(
        self_,
        requests: HostMapWidgetDefinitionRequests,
        type: HostMapWidgetDefinitionType,
        custom_links: Union[List[WidgetCustomLink], UnsetType] = unset,
        group: Union[List[str], UnsetType] = unset,
        no_group_hosts: Union[bool, UnsetType] = unset,
        no_metric_hosts: Union[bool, UnsetType] = unset,
        node_type: Union[WidgetNodeType, UnsetType] = unset,
        notes: Union[str, UnsetType] = unset,
        scope: Union[List[str], UnsetType] = unset,
        style: Union[HostMapWidgetDefinitionStyle, UnsetType] = unset,
        title: Union[str, UnsetType] = unset,
        title_align: Union[WidgetTextAlign, UnsetType] = unset,
        title_size: Union[str, UnsetType] = unset,
        **kwargs,
    ):
        """
        The host map widget graphs any metric across your hosts using the same visualization available from the main Host Map page.

        :param custom_links: List of custom links.
        :type custom_links: [WidgetCustomLink], optional

        :param group: List of tag prefixes to group by.
        :type group: [str], optional

        :param no_group_hosts: Whether to show the hosts that don’t fit in a group.
        :type no_group_hosts: bool, optional

        :param no_metric_hosts: Whether to show the hosts with no metrics.
        :type no_metric_hosts: bool, optional

        :param node_type: Which type of node to use in the map.
        :type node_type: WidgetNodeType, optional

        :param notes: Notes on the title.
        :type notes: str, optional

        :param requests: List of definitions.
        :type requests: HostMapWidgetDefinitionRequests

        :param scope: List of tags used to filter the map.
        :type scope: [str], optional

        :param style: The style to apply to the widget.
        :type style: HostMapWidgetDefinitionStyle, optional

        :param title: Title of the widget.
        :type title: str, optional

        :param title_align: How to align the text on the widget.
        :type title_align: WidgetTextAlign, optional

        :param title_size: Size of the title.
        :type title_size: str, optional

        :param type: Type of the host map widget.
        :type type: HostMapWidgetDefinitionType
        """
        if custom_links is not unset:
            kwargs["custom_links"] = custom_links
        if group is not unset:
            kwargs["group"] = group
        if no_group_hosts is not unset:
            kwargs["no_group_hosts"] = no_group_hosts
        if no_metric_hosts is not unset:
            kwargs["no_metric_hosts"] = no_metric_hosts
        if node_type is not unset:
            kwargs["node_type"] = node_type
        if notes is not unset:
            kwargs["notes"] = notes
        if scope is not unset:
            kwargs["scope"] = scope
        if style is not unset:
            kwargs["style"] = style
        if title is not unset:
            kwargs["title"] = title
        if title_align is not unset:
            kwargs["title_align"] = title_align
        if title_size is not unset:
            kwargs["title_size"] = title_size
        super().__init__(kwargs)

        self_.requests = requests
        self_.type = type
