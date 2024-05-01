# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Union, TYPE_CHECKING

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    unset,
    UnsetType,
)


if TYPE_CHECKING:
    from datadog_api_client.v2.model.ip_allowlist_entry_attributes import IPAllowlistEntryAttributes
    from datadog_api_client.v2.model.ip_allowlist_entry_type import IPAllowlistEntryType


class IPAllowlistEntryData(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.ip_allowlist_entry_attributes import IPAllowlistEntryAttributes
        from datadog_api_client.v2.model.ip_allowlist_entry_type import IPAllowlistEntryType

        return {
            "attributes": (IPAllowlistEntryAttributes,),
            "id": (str,),
            "type": (IPAllowlistEntryType,),
        }

    attribute_map = {
        "attributes": "attributes",
        "id": "id",
        "type": "type",
    }

    def __init__(
        self_,
        type: IPAllowlistEntryType,
        attributes: Union[IPAllowlistEntryAttributes, UnsetType] = unset,
        id: Union[str, UnsetType] = unset,
        **kwargs,
    ):
        """
        Data of the IP allowlist entry object.

        :param attributes: Attributes of the IP allowlist entry.
        :type attributes: IPAllowlistEntryAttributes, optional

        :param id: The unique identifier of the IP allowlist entry.
        :type id: str, optional

        :param type: IP allowlist Entry type.
        :type type: IPAllowlistEntryType
        """
        if attributes is not unset:
            kwargs["attributes"] = attributes
        if id is not unset:
            kwargs["id"] = id
        super().__init__(kwargs)

        self_.type = type
