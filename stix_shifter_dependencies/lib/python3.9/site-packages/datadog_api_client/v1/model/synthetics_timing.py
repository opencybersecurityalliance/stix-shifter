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


class SyntheticsTiming(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "dns": (float,),
            "download": (float,),
            "first_byte": (float,),
            "handshake": (float,),
            "redirect": (float,),
            "ssl": (float,),
            "tcp": (float,),
            "total": (float,),
            "wait": (float,),
        }

    attribute_map = {
        "dns": "dns",
        "download": "download",
        "first_byte": "firstByte",
        "handshake": "handshake",
        "redirect": "redirect",
        "ssl": "ssl",
        "tcp": "tcp",
        "total": "total",
        "wait": "wait",
    }

    def __init__(
        self_,
        dns: Union[float, UnsetType] = unset,
        download: Union[float, UnsetType] = unset,
        first_byte: Union[float, UnsetType] = unset,
        handshake: Union[float, UnsetType] = unset,
        redirect: Union[float, UnsetType] = unset,
        ssl: Union[float, UnsetType] = unset,
        tcp: Union[float, UnsetType] = unset,
        total: Union[float, UnsetType] = unset,
        wait: Union[float, UnsetType] = unset,
        **kwargs,
    ):
        """
        Object containing all metrics and their values collected for a Synthetic API test.
        Learn more about those metrics in `Synthetics documentation <https://docs.datadoghq.com/synthetics/#metrics>`_.

        :param dns: The duration in millisecond of the DNS lookup.
        :type dns: float, optional

        :param download: The time in millisecond to download the response.
        :type download: float, optional

        :param first_byte: The time in millisecond to first byte.
        :type first_byte: float, optional

        :param handshake: The duration in millisecond of the TLS handshake.
        :type handshake: float, optional

        :param redirect: The time in millisecond spent during redirections.
        :type redirect: float, optional

        :param ssl: The duration in millisecond of the TLS handshake.
        :type ssl: float, optional

        :param tcp: Time in millisecond to establish the TCP connection.
        :type tcp: float, optional

        :param total: The overall time in millisecond the request took to be processed.
        :type total: float, optional

        :param wait: Time spent in millisecond waiting for a response.
        :type wait: float, optional
        """
        if dns is not unset:
            kwargs["dns"] = dns
        if download is not unset:
            kwargs["download"] = download
        if first_byte is not unset:
            kwargs["first_byte"] = first_byte
        if handshake is not unset:
            kwargs["handshake"] = handshake
        if redirect is not unset:
            kwargs["redirect"] = redirect
        if ssl is not unset:
            kwargs["ssl"] = ssl
        if tcp is not unset:
            kwargs["tcp"] = tcp
        if total is not unset:
            kwargs["total"] = total
        if wait is not unset:
            kwargs["wait"] = wait
        super().__init__(kwargs)
