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


class ApiKey(ModelNormal):
    validations = {
        "key": {
            "max_length": 32,
            "min_length": 32,
        },
    }

    @cached_property
    def openapi_types(_):
        return {
            "created": (str,),
            "created_by": (str,),
            "key": (str,),
            "name": (str,),
        }

    attribute_map = {
        "created": "created",
        "created_by": "created_by",
        "key": "key",
        "name": "name",
    }
    read_only_vars = {
        "created",
        "created_by",
        "key",
    }

    def __init__(
        self_,
        created: Union[str, UnsetType] = unset,
        created_by: Union[str, UnsetType] = unset,
        key: Union[str, UnsetType] = unset,
        name: Union[str, UnsetType] = unset,
        **kwargs,
    ):
        """
        Datadog API key.

        :param created: Date of creation of the API key.
        :type created: str, optional

        :param created_by: Datadog user handle that created the API key.
        :type created_by: str, optional

        :param key: API key.
        :type key: str, optional

        :param name: Name of your API key.
        :type name: str, optional
        """
        if created is not unset:
            kwargs["created"] = created
        if created_by is not unset:
            kwargs["created_by"] = created_by
        if key is not unset:
            kwargs["key"] = key
        if name is not unset:
            kwargs["name"] = name
        super().__init__(kwargs)
