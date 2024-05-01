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


class WidgetCustomLink(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "is_hidden": (bool,),
            "label": (str,),
            "link": (str,),
            "override_label": (str,),
        }

    attribute_map = {
        "is_hidden": "is_hidden",
        "label": "label",
        "link": "link",
        "override_label": "override_label",
    }

    def __init__(
        self_,
        is_hidden: Union[bool, UnsetType] = unset,
        label: Union[str, UnsetType] = unset,
        link: Union[str, UnsetType] = unset,
        override_label: Union[str, UnsetType] = unset,
        **kwargs,
    ):
        """
        Custom links help you connect a data value to a URL, like a Datadog page or your AWS console.

        :param is_hidden: The flag for toggling context menu link visibility.
        :type is_hidden: bool, optional

        :param label: The label for the custom link URL. Keep the label short and descriptive. Use metrics and tags as variables.
        :type label: str, optional

        :param link: The URL of the custom link. URL must include ``http`` or ``https``. A relative URL must start with ``/``.
        :type link: str, optional

        :param override_label: The label ID that refers to a context menu link. Can be ``logs`` , ``hosts`` , ``traces`` , ``profiles`` , ``processes`` , ``containers`` , or ``rum``.
        :type override_label: str, optional
        """
        if is_hidden is not unset:
            kwargs["is_hidden"] = is_hidden
        if label is not unset:
            kwargs["label"] = label
        if link is not unset:
            kwargs["link"] = link
        if override_label is not unset:
            kwargs["override_label"] = override_label
        super().__init__(kwargs)
