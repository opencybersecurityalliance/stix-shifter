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
    from datadog_api_client.v1.model.slack_integration_channel_display import SlackIntegrationChannelDisplay


class SlackIntegrationChannel(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.slack_integration_channel_display import SlackIntegrationChannelDisplay

        return {
            "display": (SlackIntegrationChannelDisplay,),
            "name": (str,),
        }

    attribute_map = {
        "display": "display",
        "name": "name",
    }

    def __init__(
        self_,
        display: Union[SlackIntegrationChannelDisplay, UnsetType] = unset,
        name: Union[str, UnsetType] = unset,
        **kwargs,
    ):
        """
        The Slack channel configuration.

        :param display: Configuration options for what is shown in an alert event message.
        :type display: SlackIntegrationChannelDisplay, optional

        :param name: Your channel name.
        :type name: str, optional
        """
        if display is not unset:
            kwargs["display"] = display
        if name is not unset:
            kwargs["name"] = name
        super().__init__(kwargs)
