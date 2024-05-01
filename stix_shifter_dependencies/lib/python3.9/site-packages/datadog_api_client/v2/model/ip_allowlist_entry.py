# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import TYPE_CHECKING

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
)


if TYPE_CHECKING:
    from datadog_api_client.v2.model.ip_allowlist_entry_data import IPAllowlistEntryData


class IPAllowlistEntry(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.ip_allowlist_entry_data import IPAllowlistEntryData

        return {
            "data": (IPAllowlistEntryData,),
        }

    attribute_map = {
        "data": "data",
    }

    def __init__(self_, data: IPAllowlistEntryData, **kwargs):
        """
        IP allowlist entry object.

        :param data: Data of the IP allowlist entry object.
        :type data: IPAllowlistEntryData
        """
        super().__init__(kwargs)

        self_.data = data
