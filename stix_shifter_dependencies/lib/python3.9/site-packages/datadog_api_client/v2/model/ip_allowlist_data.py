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
    from datadog_api_client.v2.model.ip_allowlist_attributes import IPAllowlistAttributes
    from datadog_api_client.v2.model.ip_allowlist_type import IPAllowlistType


class IPAllowlistData(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.ip_allowlist_attributes import IPAllowlistAttributes
        from datadog_api_client.v2.model.ip_allowlist_type import IPAllowlistType

        return {
            "attributes": (IPAllowlistAttributes,),
            "id": (str,),
            "type": (IPAllowlistType,),
        }

    attribute_map = {
        "attributes": "attributes",
        "id": "id",
        "type": "type",
    }

    def __init__(
        self_,
        type: IPAllowlistType,
        attributes: Union[IPAllowlistAttributes, UnsetType] = unset,
        id: Union[str, UnsetType] = unset,
        **kwargs,
    ):
        """
        IP allowlist data.

        :param attributes: Attributes of the IP allowlist.
        :type attributes: IPAllowlistAttributes, optional

        :param id: The unique identifier of the org.
        :type id: str, optional

        :param type: IP allowlist type.
        :type type: IPAllowlistType
        """
        if attributes is not unset:
            kwargs["attributes"] = attributes
        if id is not unset:
            kwargs["id"] = id
        super().__init__(kwargs)

        self_.type = type
