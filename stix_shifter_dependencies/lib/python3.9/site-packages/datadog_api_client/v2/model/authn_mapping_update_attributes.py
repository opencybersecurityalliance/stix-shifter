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


class AuthNMappingUpdateAttributes(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "attribute_key": (str,),
            "attribute_value": (str,),
        }

    attribute_map = {
        "attribute_key": "attribute_key",
        "attribute_value": "attribute_value",
    }

    def __init__(
        self_, attribute_key: Union[str, UnsetType] = unset, attribute_value: Union[str, UnsetType] = unset, **kwargs
    ):
        """
        Key/Value pair of attributes used for update request.

        :param attribute_key: Key portion of a key/value pair of the attribute sent from the Identity Provider.
        :type attribute_key: str, optional

        :param attribute_value: Value portion of a key/value pair of the attribute sent from the Identity Provider.
        :type attribute_value: str, optional
        """
        if attribute_key is not unset:
            kwargs["attribute_key"] = attribute_key
        if attribute_value is not unset:
            kwargs["attribute_value"] = attribute_value
        super().__init__(kwargs)
