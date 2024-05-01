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


class TeamCreateAttributes(ModelNormal):
    validations = {
        "handle": {
            "max_length": 64,
        },
        "link_count": {
            "inclusive_maximum": 2147483647,
        },
        "name": {
            "max_length": 64,
        },
    }

    @cached_property
    def openapi_types(_):
        return {
            "description": (str,),
            "handle": (str,),
            "link_count": (int,),
            "name": (str,),
        }

    attribute_map = {
        "description": "description",
        "handle": "handle",
        "link_count": "link_count",
        "name": "name",
    }
    read_only_vars = {
        "link_count",
    }

    def __init__(
        self_,
        handle: str,
        name: str,
        description: Union[str, UnsetType] = unset,
        link_count: Union[int, UnsetType] = unset,
        **kwargs,
    ):
        """
        Team creation attributes

        :param description: Free-form markdown description/content for the team's homepage
        :type description: str, optional

        :param handle: The team's identifier
        :type handle: str

        :param link_count: The number of links belonging to the team
        :type link_count: int, optional

        :param name: The name of the team
        :type name: str
        """
        if description is not unset:
            kwargs["description"] = description
        if link_count is not unset:
            kwargs["link_count"] = link_count
        super().__init__(kwargs)

        self_.handle = handle
        self_.name = name
