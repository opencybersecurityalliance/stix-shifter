# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Union

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    datetime,
    none_type,
    unset,
    UnsetType,
)


class NotebookAuthor(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "created_at": (datetime,),
            "disabled": (bool,),
            "email": (str,),
            "handle": (str,),
            "icon": (str,),
            "name": (str, none_type),
            "status": (str,),
            "title": (str, none_type),
            "verified": (bool,),
        }

    attribute_map = {
        "created_at": "created_at",
        "disabled": "disabled",
        "email": "email",
        "handle": "handle",
        "icon": "icon",
        "name": "name",
        "status": "status",
        "title": "title",
        "verified": "verified",
    }

    def __init__(
        self_,
        created_at: Union[datetime, UnsetType] = unset,
        disabled: Union[bool, UnsetType] = unset,
        email: Union[str, UnsetType] = unset,
        handle: Union[str, UnsetType] = unset,
        icon: Union[str, UnsetType] = unset,
        name: Union[str, none_type, UnsetType] = unset,
        status: Union[str, UnsetType] = unset,
        title: Union[str, none_type, UnsetType] = unset,
        verified: Union[bool, UnsetType] = unset,
        **kwargs,
    ):
        """
        Attributes of user object returned by the API.

        :param created_at: Creation time of the user.
        :type created_at: datetime, optional

        :param disabled: Whether the user is disabled.
        :type disabled: bool, optional

        :param email: Email of the user.
        :type email: str, optional

        :param handle: Handle of the user.
        :type handle: str, optional

        :param icon: URL of the user's icon.
        :type icon: str, optional

        :param name: Name of the user.
        :type name: str, none_type, optional

        :param status: Status of the user.
        :type status: str, optional

        :param title: Title of the user.
        :type title: str, none_type, optional

        :param verified: Whether the user is verified.
        :type verified: bool, optional
        """
        if created_at is not unset:
            kwargs["created_at"] = created_at
        if disabled is not unset:
            kwargs["disabled"] = disabled
        if email is not unset:
            kwargs["email"] = email
        if handle is not unset:
            kwargs["handle"] = handle
        if icon is not unset:
            kwargs["icon"] = icon
        if name is not unset:
            kwargs["name"] = name
        if status is not unset:
            kwargs["status"] = status
        if title is not unset:
            kwargs["title"] = title
        if verified is not unset:
            kwargs["verified"] = verified
        super().__init__(kwargs)
