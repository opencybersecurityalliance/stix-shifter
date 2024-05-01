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


class UserTeamPermissionAttributes(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "permissions": (dict,),
        }

    attribute_map = {
        "permissions": "permissions",
    }
    read_only_vars = {
        "permissions",
    }

    def __init__(self_, permissions: Union[dict, UnsetType] = unset, **kwargs):
        """
        User team permission attributes

        :param permissions: Object of team permission actions and boolean values indicating of the currently logged in user can perform them on this team
        :type permissions: dict, optional
        """
        if permissions is not unset:
            kwargs["permissions"] = permissions
        super().__init__(kwargs)
