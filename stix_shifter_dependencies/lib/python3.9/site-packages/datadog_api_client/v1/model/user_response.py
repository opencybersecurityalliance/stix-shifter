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
    from datadog_api_client.v1.model.user import User


class UserResponse(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.user import User

        return {
            "user": (User,),
        }

    attribute_map = {
        "user": "user",
    }

    def __init__(self_, user: Union[User, UnsetType] = unset, **kwargs):
        """
        A Datadog User.

        :param user: Create, edit, and disable users.
        :type user: User, optional
        """
        if user is not unset:
            kwargs["user"] = user
        super().__init__(kwargs)
