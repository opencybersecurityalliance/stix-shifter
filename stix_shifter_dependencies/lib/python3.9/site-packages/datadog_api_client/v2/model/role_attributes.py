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


class RoleAttributes(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "created_at": (datetime,),
            "modified_at": (datetime,),
            "name": (str,),
            "user_count": (int,),
        }

    attribute_map = {
        "created_at": "created_at",
        "modified_at": "modified_at",
        "name": "name",
        "user_count": "user_count",
    }
    read_only_vars = {
        "created_at",
        "modified_at",
        "user_count",
    }

    def __init__(
        self_,
        created_at: Union[datetime, UnsetType] = unset,
        modified_at: Union[datetime, UnsetType] = unset,
        name: Union[str, UnsetType] = unset,
        user_count: Union[int, UnsetType] = unset,
        **kwargs,
    ):
        """
        Attributes of the role.

        :param created_at: Creation time of the role.
        :type created_at: datetime, optional

        :param modified_at: Time of last role modification.
        :type modified_at: datetime, optional

        :param name: The name of the role. The name is neither unique nor a stable identifier of the role.
        :type name: str, optional

        :param user_count: Number of users with that role.
        :type user_count: int, optional
        """
        if created_at is not unset:
            kwargs["created_at"] = created_at
        if modified_at is not unset:
            kwargs["modified_at"] = modified_at
        if name is not unset:
            kwargs["name"] = name
        if user_count is not unset:
            kwargs["user_count"] = user_count
        super().__init__(kwargs)
