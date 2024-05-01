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


class HostMuteResponse(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "action": (str,),
            "end": (int,),
            "hostname": (str,),
            "message": (str,),
        }

    attribute_map = {
        "action": "action",
        "end": "end",
        "hostname": "hostname",
        "message": "message",
    }

    def __init__(
        self_,
        action: Union[str, UnsetType] = unset,
        end: Union[int, UnsetType] = unset,
        hostname: Union[str, UnsetType] = unset,
        message: Union[str, UnsetType] = unset,
        **kwargs,
    ):
        """
        Response with the list of muted host for your organization.

        :param action: Action applied to the hosts.
        :type action: str, optional

        :param end: POSIX timestamp in seconds when the host is unmuted.
        :type end: int, optional

        :param hostname: The host name.
        :type hostname: str, optional

        :param message: Message associated with the mute.
        :type message: str, optional
        """
        if action is not unset:
            kwargs["action"] = action
        if end is not unset:
            kwargs["end"] = end
        if hostname is not unset:
            kwargs["hostname"] = hostname
        if message is not unset:
            kwargs["message"] = message
        super().__init__(kwargs)
