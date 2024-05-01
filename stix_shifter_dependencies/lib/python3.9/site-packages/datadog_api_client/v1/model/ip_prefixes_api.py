# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import List, Union

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    unset,
    UnsetType,
)


class IPPrefixesAPI(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "prefixes_ipv4": ([str],),
            "prefixes_ipv6": ([str],),
        }

    attribute_map = {
        "prefixes_ipv4": "prefixes_ipv4",
        "prefixes_ipv6": "prefixes_ipv6",
    }

    def __init__(
        self_,
        prefixes_ipv4: Union[List[str], UnsetType] = unset,
        prefixes_ipv6: Union[List[str], UnsetType] = unset,
        **kwargs,
    ):
        """
        Available prefix information for the API endpoints.

        :param prefixes_ipv4: List of IPv4 prefixes.
        :type prefixes_ipv4: [str], optional

        :param prefixes_ipv6: List of IPv6 prefixes.
        :type prefixes_ipv6: [str], optional
        """
        if prefixes_ipv4 is not unset:
            kwargs["prefixes_ipv4"] = prefixes_ipv4
        if prefixes_ipv6 is not unset:
            kwargs["prefixes_ipv6"] = prefixes_ipv6
        super().__init__(kwargs)
