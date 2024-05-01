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


class PartialApplicationKeyAttributes(ModelNormal):
    validations = {
        "last4": {
            "max_length": 4,
            "min_length": 4,
        },
    }

    @cached_property
    def openapi_types(_):
        return {
            "created_at": (str,),
            "last4": (str,),
            "name": (str,),
            "scopes": ([str], none_type),
        }

    attribute_map = {
        "created_at": "created_at",
        "last4": "last4",
        "name": "name",
        "scopes": "scopes",
    }
    read_only_vars = {
        "created_at",
        "last4",
    }

    def __init__(
        self_,
        created_at: Union[str, UnsetType] = unset,
        last4: Union[str, UnsetType] = unset,
        name: Union[str, UnsetType] = unset,
        scopes: Union[List[str], none_type, UnsetType] = unset,
        **kwargs,
    ):
        """
        Attributes of a partial application key.

        :param created_at: Creation date of the application key.
        :type created_at: str, optional

        :param last4: The last four characters of the application key.
        :type last4: str, optional

        :param name: Name of the application key.
        :type name: str, optional

        :param scopes: Array of scopes to grant the application key. This feature is in private beta, please contact Datadog support to enable scopes for your application keys.
        :type scopes: [str], none_type, optional
        """
        if created_at is not unset:
            kwargs["created_at"] = created_at
        if last4 is not unset:
            kwargs["last4"] = last4
        if name is not unset:
            kwargs["name"] = name
        if scopes is not unset:
            kwargs["scopes"] = scopes
        super().__init__(kwargs)
