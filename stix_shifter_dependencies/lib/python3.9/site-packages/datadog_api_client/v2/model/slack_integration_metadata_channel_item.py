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


class SlackIntegrationMetadataChannelItem(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "channel_id": (str,),
            "channel_name": (str,),
            "redirect_url": (str,),
            "team_id": (str,),
        }

    attribute_map = {
        "channel_id": "channel_id",
        "channel_name": "channel_name",
        "redirect_url": "redirect_url",
        "team_id": "team_id",
    }

    def __init__(
        self_, channel_id: str, channel_name: str, redirect_url: str, team_id: Union[str, UnsetType] = unset, **kwargs
    ):
        """
        Item in the Slack integration metadata channel array.

        :param channel_id: Slack channel ID.
        :type channel_id: str

        :param channel_name: Name of the Slack channel.
        :type channel_name: str

        :param redirect_url: URL redirecting to the Slack channel.
        :type redirect_url: str

        :param team_id: Slack team ID.
        :type team_id: str, optional
        """
        if team_id is not unset:
            kwargs["team_id"] = team_id
        super().__init__(kwargs)

        self_.channel_id = channel_id
        self_.channel_name = channel_name
        self_.redirect_url = redirect_url
