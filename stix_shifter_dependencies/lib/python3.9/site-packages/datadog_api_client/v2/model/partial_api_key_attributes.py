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


class PartialAPIKeyAttributes(ModelNormal):
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
            "modified_at": (str,),
            "name": (str,),
        }

    attribute_map = {
        "created_at": "created_at",
        "last4": "last4",
        "modified_at": "modified_at",
        "name": "name",
    }
    read_only_vars = {
        "created_at",
        "last4",
        "modified_at",
    }

    def __init__(
        self_,
        created_at: Union[str, UnsetType] = unset,
        last4: Union[str, UnsetType] = unset,
        modified_at: Union[str, UnsetType] = unset,
        name: Union[str, UnsetType] = unset,
        **kwargs,
    ):
        """
        Attributes of a partial API key.

        :param created_at: Creation date of the API key.
        :type created_at: str, optional

        :param last4: The last four characters of the API key.
        :type last4: str, optional

        :param modified_at: Date the API key was last modified.
        :type modified_at: str, optional

        :param name: Name of the API key.
        :type name: str, optional
        """
        if created_at is not unset:
            kwargs["created_at"] = created_at
        if last4 is not unset:
            kwargs["last4"] = last4
        if modified_at is not unset:
            kwargs["modified_at"] = modified_at
        if name is not unset:
            kwargs["name"] = name
        super().__init__(kwargs)
