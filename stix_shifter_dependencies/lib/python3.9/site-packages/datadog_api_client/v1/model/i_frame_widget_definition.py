# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import TYPE_CHECKING

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
)


if TYPE_CHECKING:
    from datadog_api_client.v1.model.i_frame_widget_definition_type import IFrameWidgetDefinitionType


class IFrameWidgetDefinition(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.i_frame_widget_definition_type import IFrameWidgetDefinitionType

        return {
            "type": (IFrameWidgetDefinitionType,),
            "url": (str,),
        }

    attribute_map = {
        "type": "type",
        "url": "url",
    }

    def __init__(self_, type: IFrameWidgetDefinitionType, url: str, **kwargs):
        """
        The iframe widget allows you to embed a portion of any other web page on your dashboard. Only available on FREE layout dashboards.

        :param type: Type of the iframe widget.
        :type type: IFrameWidgetDefinitionType

        :param url: URL of the iframe.
        :type url: str
        """
        super().__init__(kwargs)

        self_.type = type
        self_.url = url
