# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Union

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    datetime,
    unset,
    UnsetType,
)


class IPAllowlistEntryAttributes(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "cidr_block": (str,),
            "created_at": (datetime,),
            "modified_at": (datetime,),
            "note": (str,),
        }

    attribute_map = {
        "cidr_block": "cidr_block",
        "created_at": "created_at",
        "modified_at": "modified_at",
        "note": "note",
    }
    read_only_vars = {
        "created_at",
        "modified_at",
    }

    def __init__(
        self_,
        cidr_block: Union[str, UnsetType] = unset,
        created_at: Union[datetime, UnsetType] = unset,
        modified_at: Union[datetime, UnsetType] = unset,
        note: Union[str, UnsetType] = unset,
        **kwargs,
    ):
        """
        Attributes of the IP allowlist entry.

        :param cidr_block: The CIDR block describing the IP range of the entry.
        :type cidr_block: str, optional

        :param created_at: Creation time of the entry.
        :type created_at: datetime, optional

        :param modified_at: Time of last entry modification.
        :type modified_at: datetime, optional

        :param note: A note describing the IP allowlist entry.
        :type note: str, optional
        """
        if cidr_block is not unset:
            kwargs["cidr_block"] = cidr_block
        if created_at is not unset:
            kwargs["created_at"] = created_at
        if modified_at is not unset:
            kwargs["modified_at"] = modified_at
        if note is not unset:
            kwargs["note"] = note
        super().__init__(kwargs)
