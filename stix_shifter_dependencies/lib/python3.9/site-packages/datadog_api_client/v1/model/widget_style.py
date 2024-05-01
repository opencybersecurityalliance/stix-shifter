# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Union

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    unset,
    UnsetType,
)


class WidgetStyle(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "palette": (str,),
        }

    attribute_map = {
        "palette": "palette",
    }

    def __init__(self_, palette: Union[str, UnsetType] = unset, **kwargs):
        """
        Widget style definition.

        :param palette: Color palette to apply to the widget.
        :type palette: str, optional
        """
        if palette is not unset:
            kwargs["palette"] = palette
        super().__init__(kwargs)
