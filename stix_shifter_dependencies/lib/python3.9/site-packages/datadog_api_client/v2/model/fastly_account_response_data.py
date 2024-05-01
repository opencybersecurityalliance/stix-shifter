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
    from datadog_api_client.v2.model.fastly_accoun_response_attributes import FastlyAccounResponseAttributes
    from datadog_api_client.v2.model.fastly_account_type import FastlyAccountType


class FastlyAccountResponseData(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.fastly_accoun_response_attributes import FastlyAccounResponseAttributes
        from datadog_api_client.v2.model.fastly_account_type import FastlyAccountType

        return {
            "attributes": (FastlyAccounResponseAttributes,),
            "id": (str,),
            "type": (FastlyAccountType,),
        }

    attribute_map = {
        "attributes": "attributes",
        "id": "id",
        "type": "type",
    }

    def __init__(self_, attributes: FastlyAccounResponseAttributes, id: str, type: FastlyAccountType, **kwargs):
        """
        Data object of a Fastly account.

        :param attributes: Attributes object of a Fastly account.
        :type attributes: FastlyAccounResponseAttributes

        :param id: The ID of the Fastly account, a hash of the account name.
        :type id: str

        :param type: The JSON:API type for this API. Should always be ``fastly-accounts``.
        :type type: FastlyAccountType
        """
        super().__init__(kwargs)

        self_.attributes = attributes
        self_.id = id
        self_.type = type
