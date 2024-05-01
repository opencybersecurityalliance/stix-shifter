# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Union

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    none_type,
    unset,
    UnsetType,
)


class Creator(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "email": (str,),
            "handle": (str,),
            "name": (str, none_type),
        }

    attribute_map = {
        "email": "email",
        "handle": "handle",
        "name": "name",
    }

    def __init__(
        self_,
        email: Union[str, UnsetType] = unset,
        handle: Union[str, UnsetType] = unset,
        name: Union[str, none_type, UnsetType] = unset,
        **kwargs,
    ):
        """
        Object describing the creator of the shared element.

        :param email: Email of the creator.
        :type email: str, optional

        :param handle: Handle of the creator.
        :type handle: str, optional

        :param name: Name of the creator.
        :type name: str, none_type, optional
        """
        if email is not unset:
            kwargs["email"] = email
        if handle is not unset:
            kwargs["handle"] = handle
        if name is not unset:
            kwargs["name"] = name
        super().__init__(kwargs)
