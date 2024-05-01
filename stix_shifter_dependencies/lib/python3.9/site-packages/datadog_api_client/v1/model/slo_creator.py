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


class SLOCreator(ModelNormal):
    _nullable = True

    @cached_property
    def openapi_types(_):
        return {
            "email": (str,),
            "id": (int,),
            "name": (str, none_type),
        }

    attribute_map = {
        "email": "email",
        "id": "id",
        "name": "name",
    }

    def __init__(
        self_,
        email: Union[str, UnsetType] = unset,
        id: Union[int, UnsetType] = unset,
        name: Union[str, none_type, UnsetType] = unset,
        **kwargs,
    ):
        """
        The creator of the SLO

        :param email: Email of the creator.
        :type email: str, optional

        :param id: User ID of the creator.
        :type id: int, optional

        :param name: Name of the creator.
        :type name: str, none_type, optional
        """
        if email is not unset:
            kwargs["email"] = email
        if id is not unset:
            kwargs["id"] = id
        if name is not unset:
            kwargs["name"] = name
        super().__init__(kwargs)
