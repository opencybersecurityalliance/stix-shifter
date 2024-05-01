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


class ApplicationKeyCreateAttributes(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "name": (str,),
            "scopes": ([str], none_type),
        }

    attribute_map = {
        "name": "name",
        "scopes": "scopes",
    }

    def __init__(self_, name: str, scopes: Union[List[str], none_type, UnsetType] = unset, **kwargs):
        """
        Attributes used to create an application Key.

        :param name: Name of the application key.
        :type name: str

        :param scopes: Array of scopes to grant the application key. This feature is in private beta, please contact Datadog support to enable scopes for your application keys.
        :type scopes: [str], none_type, optional
        """
        if scopes is not unset:
            kwargs["scopes"] = scopes
        super().__init__(kwargs)

        self_.name = name
