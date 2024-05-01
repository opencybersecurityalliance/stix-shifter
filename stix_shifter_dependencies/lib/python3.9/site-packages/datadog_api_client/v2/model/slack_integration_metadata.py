# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import List, TYPE_CHECKING

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
)


if TYPE_CHECKING:
    from datadog_api_client.v2.model.slack_integration_metadata_channel_item import SlackIntegrationMetadataChannelItem


class SlackIntegrationMetadata(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.slack_integration_metadata_channel_item import (
            SlackIntegrationMetadataChannelItem,
        )

        return {
            "channels": ([SlackIntegrationMetadataChannelItem],),
        }

    attribute_map = {
        "channels": "channels",
    }

    def __init__(self_, channels: List[SlackIntegrationMetadataChannelItem], **kwargs):
        """
        Incident integration metadata for the Slack integration.

        :param channels: Array of Slack channels in this integration metadata.
        :type channels: [SlackIntegrationMetadataChannelItem]
        """
        super().__init__(kwargs)

        self_.channels = channels
