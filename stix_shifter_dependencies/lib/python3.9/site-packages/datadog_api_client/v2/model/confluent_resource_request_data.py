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
    from datadog_api_client.v2.model.confluent_resource_request_attributes import ConfluentResourceRequestAttributes
    from datadog_api_client.v2.model.confluent_resource_type import ConfluentResourceType


class ConfluentResourceRequestData(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.confluent_resource_request_attributes import ConfluentResourceRequestAttributes
        from datadog_api_client.v2.model.confluent_resource_type import ConfluentResourceType

        return {
            "attributes": (ConfluentResourceRequestAttributes,),
            "id": (str,),
            "type": (ConfluentResourceType,),
        }

    attribute_map = {
        "attributes": "attributes",
        "id": "id",
        "type": "type",
    }

    def __init__(self_, attributes: ConfluentResourceRequestAttributes, id: str, type: ConfluentResourceType, **kwargs):
        """
        JSON:API request for updating a Confluent resource.

        :param attributes: Attributes object for updating a Confluent resource.
        :type attributes: ConfluentResourceRequestAttributes

        :param id: The ID associated with a Confluent resource.
        :type id: str

        :param type: The JSON:API type for this request.
        :type type: ConfluentResourceType
        """
        super().__init__(kwargs)

        self_.attributes = attributes
        self_.id = id
        self_.type = type
