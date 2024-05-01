# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
)


class GeomapWidgetDefinitionView(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "focus": (str,),
        }

    attribute_map = {
        "focus": "focus",
    }

    def __init__(self_, focus: str, **kwargs):
        """
        The view of the world that the map should render.

        :param focus: The 2-letter ISO code of a country to focus the map on. Or ``WORLD``.
        :type focus: str
        """
        super().__init__(kwargs)

        self_.focus = focus
