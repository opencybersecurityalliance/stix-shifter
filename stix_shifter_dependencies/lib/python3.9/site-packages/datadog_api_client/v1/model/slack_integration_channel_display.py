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


class SlackIntegrationChannelDisplay(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "message": (bool,),
            "notified": (bool,),
            "snapshot": (bool,),
            "tags": (bool,),
        }

    attribute_map = {
        "message": "message",
        "notified": "notified",
        "snapshot": "snapshot",
        "tags": "tags",
    }

    def __init__(
        self_,
        message: Union[bool, UnsetType] = unset,
        notified: Union[bool, UnsetType] = unset,
        snapshot: Union[bool, UnsetType] = unset,
        tags: Union[bool, UnsetType] = unset,
        **kwargs,
    ):
        """
        Configuration options for what is shown in an alert event message.

        :param message: Show the main body of the alert event.
        :type message: bool, optional

        :param notified: Show the list of @-handles in the alert event.
        :type notified: bool, optional

        :param snapshot: Show the alert event's snapshot image.
        :type snapshot: bool, optional

        :param tags: Show the scopes on which the monitor alerted.
        :type tags: bool, optional
        """
        if message is not unset:
            kwargs["message"] = message
        if notified is not unset:
            kwargs["notified"] = notified
        if snapshot is not unset:
            kwargs["snapshot"] = snapshot
        if tags is not unset:
            kwargs["tags"] = tags
        super().__init__(kwargs)
