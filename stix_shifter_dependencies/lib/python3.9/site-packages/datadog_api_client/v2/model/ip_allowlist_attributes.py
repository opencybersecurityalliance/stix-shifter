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
    from datadog_api_client.v2.model.ip_allowlist_entry import IPAllowlistEntry


class IPAllowlistAttributes(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.ip_allowlist_entry import IPAllowlistEntry

        return {
            "enabled": (bool,),
            "entries": ([IPAllowlistEntry],),
        }

    attribute_map = {
        "enabled": "enabled",
        "entries": "entries",
    }

    def __init__(
        self_,
        enabled: Union[bool, UnsetType] = unset,
        entries: Union[List[IPAllowlistEntry], UnsetType] = unset,
        **kwargs,
    ):
        """
        Attributes of the IP allowlist.

        :param enabled: Whether the IP allowlist logic is enabled or not.
        :type enabled: bool, optional

        :param entries: Array of entries in the IP allowlist.
        :type entries: [IPAllowlistEntry], optional
        """
        if enabled is not unset:
            kwargs["enabled"] = enabled
        if entries is not unset:
            kwargs["entries"] = entries
        super().__init__(kwargs)
