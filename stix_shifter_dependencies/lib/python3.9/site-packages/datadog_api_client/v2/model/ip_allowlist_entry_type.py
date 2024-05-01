# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class IPAllowlistEntryType(ModelSimple):
    """
    IP allowlist Entry type.

    :param value: If omitted defaults to "ip_allowlist_entry". Must be one of ["ip_allowlist_entry"].
    :type value: str
    """

    allowed_values = {
        "ip_allowlist_entry",
    }
    IP_ALLOWLIST_ENTRY: ClassVar["IPAllowlistEntryType"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


IPAllowlistEntryType.IP_ALLOWLIST_ENTRY = IPAllowlistEntryType("ip_allowlist_entry")
