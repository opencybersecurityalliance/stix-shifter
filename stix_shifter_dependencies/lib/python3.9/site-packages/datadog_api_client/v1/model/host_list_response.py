# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import List, Union, TYPE_CHECKING

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    unset,
    UnsetType,
)


if TYPE_CHECKING:
    from datadog_api_client.v1.model.host import Host


class HostListResponse(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.host import Host

        return {
            "host_list": ([Host],),
            "total_matching": (int,),
            "total_returned": (int,),
        }

    attribute_map = {
        "host_list": "host_list",
        "total_matching": "total_matching",
        "total_returned": "total_returned",
    }

    def __init__(
        self_,
        host_list: Union[List[Host], UnsetType] = unset,
        total_matching: Union[int, UnsetType] = unset,
        total_returned: Union[int, UnsetType] = unset,
        **kwargs,
    ):
        """
        Response with Host information from Datadog.

        :param host_list: Array of hosts.
        :type host_list: [Host], optional

        :param total_matching: Number of host matching the query.
        :type total_matching: int, optional

        :param total_returned: Number of host returned.
        :type total_returned: int, optional
        """
        if host_list is not unset:
            kwargs["host_list"] = host_list
        if total_matching is not unset:
            kwargs["total_matching"] = total_matching
        if total_returned is not unset:
            kwargs["total_returned"] = total_returned
        super().__init__(kwargs)
