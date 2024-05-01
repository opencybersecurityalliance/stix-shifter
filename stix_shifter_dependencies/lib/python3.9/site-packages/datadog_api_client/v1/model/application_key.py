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


class ApplicationKey(ModelNormal):
    validations = {
        "hash": {
            "max_length": 40,
            "min_length": 40,
        },
    }

    @cached_property
    def openapi_types(_):
        return {
            "hash": (str,),
            "name": (str,),
            "owner": (str,),
        }

    attribute_map = {
        "hash": "hash",
        "name": "name",
        "owner": "owner",
    }
    read_only_vars = {
        "hash",
        "owner",
    }

    def __init__(
        self_,
        hash: Union[str, UnsetType] = unset,
        name: Union[str, UnsetType] = unset,
        owner: Union[str, UnsetType] = unset,
        **kwargs,
    ):
        """
        An application key with its associated metadata.

        :param hash: Hash of an application key.
        :type hash: str, optional

        :param name: Name of an application key.
        :type name: str, optional

        :param owner: Owner of an application key.
        :type owner: str, optional
        """
        if hash is not unset:
            kwargs["hash"] = hash
        if name is not unset:
            kwargs["name"] = name
        if owner is not unset:
            kwargs["owner"] = owner
        super().__init__(kwargs)
