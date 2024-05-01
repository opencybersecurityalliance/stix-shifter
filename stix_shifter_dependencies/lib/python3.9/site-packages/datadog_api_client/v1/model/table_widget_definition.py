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
    from datadog_api_client.v1.model.table_widget_has_search_bar import TableWidgetHasSearchBar
    from datadog_api_client.v1.model.table_widget_request import TableWidgetRequest
    from datadog_api_client.v1.model.widget_time import WidgetTime
    from datadog_api_client.v1.model.widget_text_align import WidgetTextAlign
    from datadog_api_client.v1.model.table_widget_definition_type import TableWidgetDefinitionType


class TableWidgetDefinition(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.widget_custom_link import WidgetCustomLink
        from datadog_api_client.v1.model.table_widget_has_search_bar import TableWidgetHasSearchBar
        from datadog_api_client.v1.model.table_widget_request import TableWidgetRequest
        from datadog_api_client.v1.model.widget_time import WidgetTime
        from datadog_api_client.v1.model.widget_text_align import WidgetTextAlign
        from datadog_api_client.v1.model.table_widget_definition_type import TableWidgetDefinitionType

        return {
            "custom_links": ([WidgetCustomLink],),
            "has_search_bar": (TableWidgetHasSearchBar,),
            "requests": ([TableWidgetRequest],),
            "time": (WidgetTime,),
            "title": (str,),
            "title_align": (WidgetTextAlign,),
            "title_size": (str,),
            "type": (TableWidgetDefinitionType,),
        }

    attribute_map = {
        "custom_links": "custom_links",
        "has_search_bar": "has_search_bar",
        "requests": "requests",
        "time": "time",
        "title": "title",
        "title_align": "title_align",
        "title_size": "title_size",
        "type": "type",
    }

    def __init__(
        self_,
        requests: List[TableWidgetRequest],
        type: TableWidgetDefinitionType,
        custom_links: Union[List[WidgetCustomLink], UnsetType] = unset,
        has_search_bar: Union[TableWidgetHasSearchBar, UnsetType] = unset,
        time: Union[WidgetTime, UnsetType] = unset,
        title: Union[str, UnsetType] = unset,
        title_align: Union[WidgetTextAlign, UnsetType] = unset,
        title_size: Union[str, UnsetType] = unset,
        **kwargs,
    ):
        """
        The table visualization is available on timeboards and screenboards. It displays columns of metrics grouped by tag key.

        :param custom_links: List of custom links.
        :type custom_links: [WidgetCustomLink], optional

        :param has_search_bar: Controls the display of the search bar.
        :type has_search_bar: TableWidgetHasSearchBar, optional

        :param requests: Widget definition.
        :type requests: [TableWidgetRequest]

        :param time: Time setting for the widget.
        :type time: WidgetTime, optional

        :param title: Title of your widget.
        :type title: str, optional

        :param title_align: How to align the text on the widget.
        :type title_align: WidgetTextAlign, optional

        :param title_size: Size of the title.
        :type title_size: str, optional

        :param type: Type of the table widget.
        :type type: TableWidgetDefinitionType
        """
        if custom_links is not unset:
            kwargs["custom_links"] = custom_links
        if has_search_bar is not unset:
            kwargs["has_search_bar"] = has_search_bar
        if time is not unset:
            kwargs["time"] = time
        if title is not unset:
            kwargs["title"] = title
        if title_align is not unset:
            kwargs["title_align"] = title_align
        if title_size is not unset:
            kwargs["title_size"] = title_size
        super().__init__(kwargs)

        self_.requests = requests
        self_.type = type
