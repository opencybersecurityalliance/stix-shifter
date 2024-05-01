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
    from datadog_api_client.v1.model.widget_text_align import WidgetTextAlign
    from datadog_api_client.v1.model.service_map_widget_definition_type import ServiceMapWidgetDefinitionType


class ServiceMapWidgetDefinition(ModelNormal):
    validations = {
        "filters": {
            "min_items": 1,
        },
    }

    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.widget_custom_link import WidgetCustomLink
        from datadog_api_client.v1.model.widget_text_align import WidgetTextAlign
        from datadog_api_client.v1.model.service_map_widget_definition_type import ServiceMapWidgetDefinitionType

        return {
            "custom_links": ([WidgetCustomLink],),
            "filters": ([str],),
            "service": (str,),
            "title": (str,),
            "title_align": (WidgetTextAlign,),
            "title_size": (str,),
            "type": (ServiceMapWidgetDefinitionType,),
        }

    attribute_map = {
        "custom_links": "custom_links",
        "filters": "filters",
        "service": "service",
        "title": "title",
        "title_align": "title_align",
        "title_size": "title_size",
        "type": "type",
    }

    def __init__(
        self_,
        filters: List[str],
        service: str,
        type: ServiceMapWidgetDefinitionType,
        custom_links: Union[List[WidgetCustomLink], UnsetType] = unset,
        title: Union[str, UnsetType] = unset,
        title_align: Union[WidgetTextAlign, UnsetType] = unset,
        title_size: Union[str, UnsetType] = unset,
        **kwargs,
    ):
        """
        This widget displays a map of a service to all of the services that call it, and all of the services that it calls.

        :param custom_links: List of custom links.
        :type custom_links: [WidgetCustomLink], optional

        :param filters: Your environment and primary tag (or * if enabled for your account).
        :type filters: [str]

        :param service: The ID of the service you want to map.
        :type service: str

        :param title: The title of your widget.
        :type title: str, optional

        :param title_align: How to align the text on the widget.
        :type title_align: WidgetTextAlign, optional

        :param title_size: Size of the title.
        :type title_size: str, optional

        :param type: Type of the service map widget.
        :type type: ServiceMapWidgetDefinitionType
        """
        if custom_links is not unset:
            kwargs["custom_links"] = custom_links
        if title is not unset:
            kwargs["title"] = title
        if title_align is not unset:
            kwargs["title_align"] = title_align
        if title_size is not unset:
            kwargs["title_size"] = title_size
        super().__init__(kwargs)

        self_.filters = filters
        self_.service = service
        self_.type = type
