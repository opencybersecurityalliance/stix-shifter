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
    from datadog_api_client.v2.model.api_key_update_attributes import APIKeyUpdateAttributes
    from datadog_api_client.v2.model.api_keys_type import APIKeysType


class APIKeyUpdateData(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.api_key_update_attributes import APIKeyUpdateAttributes
        from datadog_api_client.v2.model.api_keys_type import APIKeysType

        return {
            "attributes": (APIKeyUpdateAttributes,),
            "id": (str,),
            "type": (APIKeysType,),
        }

    attribute_map = {
        "attributes": "attributes",
        "id": "id",
        "type": "type",
    }

    def __init__(self_, attributes: APIKeyUpdateAttributes, id: str, type: APIKeysType, **kwargs):
        """
        Object used to update an API key.

        :param attributes: Attributes used to update an API Key.
        :type attributes: APIKeyUpdateAttributes

        :param id: ID of the API key.
        :type id: str

        :param type: API Keys resource type.
        :type type: APIKeysType
        """
        super().__init__(kwargs)

        self_.attributes = attributes
        self_.id = id
        self_.type = type
