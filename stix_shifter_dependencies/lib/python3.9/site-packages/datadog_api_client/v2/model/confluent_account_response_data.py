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
    from datadog_api_client.v2.model.confluent_account_response_attributes import ConfluentAccountResponseAttributes
    from datadog_api_client.v2.model.confluent_account_type import ConfluentAccountType


class ConfluentAccountResponseData(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.confluent_account_response_attributes import ConfluentAccountResponseAttributes
        from datadog_api_client.v2.model.confluent_account_type import ConfluentAccountType

        return {
            "attributes": (ConfluentAccountResponseAttributes,),
            "id": (str,),
            "type": (ConfluentAccountType,),
        }

    attribute_map = {
        "attributes": "attributes",
        "id": "id",
        "type": "type",
    }

    def __init__(self_, attributes: ConfluentAccountResponseAttributes, id: str, type: ConfluentAccountType, **kwargs):
        """
        An API key and API secret pair that represents a Confluent account.

        :param attributes: The attributes of a Confluent account.
        :type attributes: ConfluentAccountResponseAttributes

        :param id: A randomly generated ID associated with a Confluent account.
        :type id: str

        :param type: The JSON:API type for this API. Should always be ``confluent-cloud-accounts``.
        :type type: ConfluentAccountType
        """
        super().__init__(kwargs)

        self_.attributes = attributes
        self_.id = id
        self_.type = type
