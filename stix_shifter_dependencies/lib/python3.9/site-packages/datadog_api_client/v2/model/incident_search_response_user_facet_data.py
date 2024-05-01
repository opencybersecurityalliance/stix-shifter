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


class IncidentSearchResponseUserFacetData(ModelNormal):
    validations = {
        "count": {
            "inclusive_maximum": 2147483647,
        },
    }

    @cached_property
    def openapi_types(_):
        return {
            "count": (int,),
            "email": (str,),
            "handle": (str,),
            "name": (str,),
            "uuid": (str,),
        }

    attribute_map = {
        "count": "count",
        "email": "email",
        "handle": "handle",
        "name": "name",
        "uuid": "uuid",
    }

    def __init__(
        self_,
        count: Union[int, UnsetType] = unset,
        email: Union[str, UnsetType] = unset,
        handle: Union[str, UnsetType] = unset,
        name: Union[str, UnsetType] = unset,
        uuid: Union[str, UnsetType] = unset,
        **kwargs,
    ):
        """
        Facet data for user attributes of an incident.

        :param count: Count of the facet value appearing in search results.
        :type count: int, optional

        :param email: Email of the user.
        :type email: str, optional

        :param handle: Handle of the user.
        :type handle: str, optional

        :param name: Name of the user.
        :type name: str, optional

        :param uuid: ID of the user.
        :type uuid: str, optional
        """
        if count is not unset:
            kwargs["count"] = count
        if email is not unset:
            kwargs["email"] = email
        if handle is not unset:
            kwargs["handle"] = handle
        if name is not unset:
            kwargs["name"] = name
        if uuid is not unset:
            kwargs["uuid"] = uuid
        super().__init__(kwargs)
