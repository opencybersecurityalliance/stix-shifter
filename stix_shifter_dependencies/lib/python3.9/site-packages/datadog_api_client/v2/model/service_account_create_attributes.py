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


class ServiceAccountCreateAttributes(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "email": (str,),
            "name": (str,),
            "service_account": (bool,),
            "title": (str,),
        }

    attribute_map = {
        "email": "email",
        "name": "name",
        "service_account": "service_account",
        "title": "title",
    }

    def __init__(
        self_,
        email: str,
        service_account: bool,
        name: Union[str, UnsetType] = unset,
        title: Union[str, UnsetType] = unset,
        **kwargs,
    ):
        """
        Attributes of the created user.

        :param email: The email of the user.
        :type email: str

        :param name: The name of the user.
        :type name: str, optional

        :param service_account: Whether the user is a service account. Must be true.
        :type service_account: bool

        :param title: The title of the user.
        :type title: str, optional
        """
        if name is not unset:
            kwargs["name"] = name
        if title is not unset:
            kwargs["title"] = title
        super().__init__(kwargs)

        self_.email = email
        self_.service_account = service_account
