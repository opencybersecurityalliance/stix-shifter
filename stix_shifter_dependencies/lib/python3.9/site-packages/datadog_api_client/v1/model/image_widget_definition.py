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
    from datadog_api_client.v1.model.widget_horizontal_align import WidgetHorizontalAlign
    from datadog_api_client.v1.model.widget_margin import WidgetMargin
    from datadog_api_client.v1.model.widget_image_sizing import WidgetImageSizing
    from datadog_api_client.v1.model.image_widget_definition_type import ImageWidgetDefinitionType
    from datadog_api_client.v1.model.widget_vertical_align import WidgetVerticalAlign


class ImageWidgetDefinition(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.widget_horizontal_align import WidgetHorizontalAlign
        from datadog_api_client.v1.model.widget_margin import WidgetMargin
        from datadog_api_client.v1.model.widget_image_sizing import WidgetImageSizing
        from datadog_api_client.v1.model.image_widget_definition_type import ImageWidgetDefinitionType
        from datadog_api_client.v1.model.widget_vertical_align import WidgetVerticalAlign

        return {
            "has_background": (bool,),
            "has_border": (bool,),
            "horizontal_align": (WidgetHorizontalAlign,),
            "margin": (WidgetMargin,),
            "sizing": (WidgetImageSizing,),
            "type": (ImageWidgetDefinitionType,),
            "url": (str,),
            "url_dark_theme": (str,),
            "vertical_align": (WidgetVerticalAlign,),
        }

    attribute_map = {
        "has_background": "has_background",
        "has_border": "has_border",
        "horizontal_align": "horizontal_align",
        "margin": "margin",
        "sizing": "sizing",
        "type": "type",
        "url": "url",
        "url_dark_theme": "url_dark_theme",
        "vertical_align": "vertical_align",
    }

    def __init__(
        self_,
        type: ImageWidgetDefinitionType,
        url: str,
        has_background: Union[bool, UnsetType] = unset,
        has_border: Union[bool, UnsetType] = unset,
        horizontal_align: Union[WidgetHorizontalAlign, UnsetType] = unset,
        margin: Union[WidgetMargin, UnsetType] = unset,
        sizing: Union[WidgetImageSizing, UnsetType] = unset,
        url_dark_theme: Union[str, UnsetType] = unset,
        vertical_align: Union[WidgetVerticalAlign, UnsetType] = unset,
        **kwargs,
    ):
        """
        The image widget allows you to embed an image on your dashboard. An image can be a PNG, JPG, or animated GIF. Only available on FREE layout dashboards.

        :param has_background: Whether to display a background or not.
        :type has_background: bool, optional

        :param has_border: Whether to display a border or not.
        :type has_border: bool, optional

        :param horizontal_align: Horizontal alignment.
        :type horizontal_align: WidgetHorizontalAlign, optional

        :param margin: Size of the margins around the image.
            **Note** : ``small`` and ``large`` values are deprecated.
        :type margin: WidgetMargin, optional

        :param sizing: How to size the image on the widget. The values are based on the image ``object-fit`` CSS properties.
            **Note** : ``zoom`` , ``fit`` and ``center`` values are deprecated.
        :type sizing: WidgetImageSizing, optional

        :param type: Type of the image widget.
        :type type: ImageWidgetDefinitionType

        :param url: URL of the image.
        :type url: str

        :param url_dark_theme: URL of the image in dark mode.
        :type url_dark_theme: str, optional

        :param vertical_align: Vertical alignment.
        :type vertical_align: WidgetVerticalAlign, optional
        """
        if has_background is not unset:
            kwargs["has_background"] = has_background
        if has_border is not unset:
            kwargs["has_border"] = has_border
        if horizontal_align is not unset:
            kwargs["horizontal_align"] = horizontal_align
        if margin is not unset:
            kwargs["margin"] = margin
        if sizing is not unset:
            kwargs["sizing"] = sizing
        if url_dark_theme is not unset:
            kwargs["url_dark_theme"] = url_dark_theme
        if vertical_align is not unset:
            kwargs["vertical_align"] = vertical_align
        super().__init__(kwargs)

        self_.type = type
        self_.url = url
