# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import List, Union

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    none_type,
    unset,
    UnsetType,
)


class SelectableTemplateVariableItems(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "default_value": (str,),
            "name": (str,),
            "prefix": (str,),
            "visible_tags": ([str], none_type),
        }

    attribute_map = {
        "default_value": "default_value",
        "name": "name",
        "prefix": "prefix",
        "visible_tags": "visible_tags",
    }

    def __init__(
        self_,
        default_value: Union[str, UnsetType] = unset,
        name: Union[str, UnsetType] = unset,
        prefix: Union[str, UnsetType] = unset,
        visible_tags: Union[List[str], none_type, UnsetType] = unset,
        **kwargs,
    ):
        """
        Object containing the template variable's name, associated tag/attribute, default value and selectable values.

        :param default_value: The default value of the template variable.
        :type default_value: str, optional

        :param name: Name of the template variable.
        :type name: str, optional

        :param prefix: The tag/attribute key associated with the template variable.
        :type prefix: str, optional

        :param visible_tags: List of visible tag values on the shared dashboard.
        :type visible_tags: [str], none_type, optional
        """
        if default_value is not unset:
            kwargs["default_value"] = default_value
        if name is not unset:
            kwargs["name"] = name
        if prefix is not unset:
            kwargs["prefix"] = prefix
        if visible_tags is not unset:
            kwargs["visible_tags"] = visible_tags
        super().__init__(kwargs)
