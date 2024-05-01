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
    from datadog_api_client.v1.model.geomap_widget_request import GeomapWidgetRequest
    from datadog_api_client.v1.model.geomap_widget_definition_style import GeomapWidgetDefinitionStyle
    from datadog_api_client.v1.model.widget_time import WidgetTime
    from datadog_api_client.v1.model.widget_text_align import WidgetTextAlign
    from datadog_api_client.v1.model.geomap_widget_definition_type import GeomapWidgetDefinitionType
    from datadog_api_client.v1.model.geomap_widget_definition_view import GeomapWidgetDefinitionView


class GeomapWidgetDefinition(ModelNormal):
    validations = {
        "requests": {
            "max_items": 1,
            "min_items": 1,
        },
    }

    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.widget_custom_link import WidgetCustomLink
        from datadog_api_client.v1.model.geomap_widget_request import GeomapWidgetRequest
        from datadog_api_client.v1.model.geomap_widget_definition_style import GeomapWidgetDefinitionStyle
        from datadog_api_client.v1.model.widget_time import WidgetTime
        from datadog_api_client.v1.model.widget_text_align import WidgetTextAlign
        from datadog_api_client.v1.model.geomap_widget_definition_type import GeomapWidgetDefinitionType
        from datadog_api_client.v1.model.geomap_widget_definition_view import GeomapWidgetDefinitionView

        return {
            "custom_links": ([WidgetCustomLink],),
            "requests": ([GeomapWidgetRequest],),
            "style": (GeomapWidgetDefinitionStyle,),
            "time": (WidgetTime,),
            "title": (str,),
            "title_align": (WidgetTextAlign,),
            "title_size": (str,),
            "type": (GeomapWidgetDefinitionType,),
            "view": (GeomapWidgetDefinitionView,),
        }

    attribute_map = {
        "custom_links": "custom_links",
        "requests": "requests",
        "style": "style",
        "time": "time",
        "title": "title",
        "title_align": "title_align",
        "title_size": "title_size",
        "type": "type",
        "view": "view",
    }

    def __init__(
        self_,
        requests: List[GeomapWidgetRequest],
        style: GeomapWidgetDefinitionStyle,
        type: GeomapWidgetDefinitionType,
        view: GeomapWidgetDefinitionView,
        custom_links: Union[List[WidgetCustomLink], UnsetType] = unset,
        time: Union[WidgetTime, UnsetType] = unset,
        title: Union[str, UnsetType] = unset,
        title_align: Union[WidgetTextAlign, UnsetType] = unset,
        title_size: Union[str, UnsetType] = unset,
        **kwargs,
    ):
        """
        This visualization displays a series of values by country on a world map.

        :param custom_links: A list of custom links.
        :type custom_links: [WidgetCustomLink], optional

        :param requests: Array of one request object to display in the widget. The request must contain a ``group-by`` tag whose value is a country ISO code.

            See the `Request JSON schema documentation <https://docs.datadoghq.com/dashboards/graphing_json/request_json>`_
            for information about building the ``REQUEST_SCHEMA``.
        :type requests: [GeomapWidgetRequest]

        :param style: The style to apply to the widget.
        :type style: GeomapWidgetDefinitionStyle

        :param time: Time setting for the widget.
        :type time: WidgetTime, optional

        :param title: The title of your widget.
        :type title: str, optional

        :param title_align: How to align the text on the widget.
        :type title_align: WidgetTextAlign, optional

        :param title_size: The size of the title.
        :type title_size: str, optional

        :param type: Type of the geomap widget.
        :type type: GeomapWidgetDefinitionType

        :param view: The view of the world that the map should render.
        :type view: GeomapWidgetDefinitionView
        """
        if custom_links is not unset:
            kwargs["custom_links"] = custom_links
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
        self_.style = style
        self_.type = type
        self_.view = view
