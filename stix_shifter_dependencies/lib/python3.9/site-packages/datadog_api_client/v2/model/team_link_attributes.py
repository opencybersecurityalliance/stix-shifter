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


class TeamLinkAttributes(ModelNormal):
    validations = {
        "label": {
            "max_length": 256,
        },
        "position": {
            "inclusive_maximum": 2147483647,
        },
    }

    @cached_property
    def openapi_types(_):
        return {
            "label": (str,),
            "position": (int,),
            "team_id": (str,),
            "url": (str,),
        }

    attribute_map = {
        "label": "label",
        "position": "position",
        "team_id": "team_id",
        "url": "url",
    }
    read_only_vars = {
        "team_id",
    }

    def __init__(
        self_,
        label: str,
        url: str,
        position: Union[int, UnsetType] = unset,
        team_id: Union[str, UnsetType] = unset,
        **kwargs,
    ):
        """
        Team link attributes

        :param label: The link's label
        :type label: str

        :param position: The link's position, used to sort links for the team
        :type position: int, optional

        :param team_id: ID of the team the link is associated with
        :type team_id: str, optional

        :param url: The URL for the link
        :type url: str
        """
        if position is not unset:
            kwargs["position"] = position
        if team_id is not unset:
            kwargs["team_id"] = team_id
        super().__init__(kwargs)

        self_.label = label
        self_.url = url
