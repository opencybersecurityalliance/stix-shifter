# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Union, TYPE_CHECKING

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    unset,
    UnsetType,
)


if TYPE_CHECKING:
    from datadog_api_client.v1.model.access_role import AccessRole


class User(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.access_role import AccessRole

        return {
            "access_role": (AccessRole,),
            "disabled": (bool,),
            "email": (str,),
            "handle": (str,),
            "icon": (str,),
            "name": (str,),
            "verified": (bool,),
        }

    attribute_map = {
        "access_role": "access_role",
        "disabled": "disabled",
        "email": "email",
        "handle": "handle",
        "icon": "icon",
        "name": "name",
        "verified": "verified",
    }
    read_only_vars = {
        "icon",
        "verified",
    }

    def __init__(
        self_,
        access_role: Union[AccessRole, UnsetType] = unset,
        disabled: Union[bool, UnsetType] = unset,
        email: Union[str, UnsetType] = unset,
        handle: Union[str, UnsetType] = unset,
        icon: Union[str, UnsetType] = unset,
        name: Union[str, UnsetType] = unset,
        verified: Union[bool, UnsetType] = unset,
        **kwargs,
    ):
        """
        Create, edit, and disable users.

        :param access_role: The access role of the user. Options are **st** (standard user), **adm** (admin user), or **ro** (read-only user).
        :type access_role: AccessRole, optional

        :param disabled: The new disabled status of the user.
        :type disabled: bool, optional

        :param email: The new email of the user.
        :type email: str, optional

        :param handle: The user handle, must be a valid email.
        :type handle: str, optional

        :param icon: Gravatar icon associated to the user.
        :type icon: str, optional

        :param name: The name of the user.
        :type name: str, optional

        :param verified: Whether or not the user logged in Datadog at least once.
        :type verified: bool, optional
        """
        if access_role is not unset:
            kwargs["access_role"] = access_role
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
        if verified is not unset:
            kwargs["verified"] = verified
        super().__init__(kwargs)
