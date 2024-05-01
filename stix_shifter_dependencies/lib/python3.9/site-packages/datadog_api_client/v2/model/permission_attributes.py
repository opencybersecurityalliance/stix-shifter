# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Union

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    datetime,
    unset,
    UnsetType,
)


class PermissionAttributes(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "created": (datetime,),
            "description": (str,),
            "display_name": (str,),
            "display_type": (str,),
            "group_name": (str,),
            "name": (str,),
            "restricted": (bool,),
        }

    attribute_map = {
        "created": "created",
        "description": "description",
        "display_name": "display_name",
        "display_type": "display_type",
        "group_name": "group_name",
        "name": "name",
        "restricted": "restricted",
    }

    def __init__(
        self_,
        created: Union[datetime, UnsetType] = unset,
        description: Union[str, UnsetType] = unset,
        display_name: Union[str, UnsetType] = unset,
        display_type: Union[str, UnsetType] = unset,
        group_name: Union[str, UnsetType] = unset,
        name: Union[str, UnsetType] = unset,
        restricted: Union[bool, UnsetType] = unset,
        **kwargs,
    ):
        """
        Attributes of a permission.

        :param created: Creation time of the permission.
        :type created: datetime, optional

        :param description: Description of the permission.
        :type description: str, optional

        :param display_name: Displayed name for the permission.
        :type display_name: str, optional

        :param display_type: Display type.
        :type display_type: str, optional

        :param group_name: Name of the permission group.
        :type group_name: str, optional

        :param name: Name of the permission.
        :type name: str, optional

        :param restricted: Whether or not the permission is restricted.
        :type restricted: bool, optional
        """
        if created is not unset:
            kwargs["created"] = created
        if description is not unset:
            kwargs["description"] = description
        if display_name is not unset:
            kwargs["display_name"] = display_name
        if display_type is not unset:
            kwargs["display_type"] = display_type
        if group_name is not unset:
            kwargs["group_name"] = group_name
        if name is not unset:
            kwargs["name"] = name
        if restricted is not unset:
            kwargs["restricted"] = restricted
        super().__init__(kwargs)
