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
    from datadog_api_client.v2.model.cloudflare_account_response_attributes import CloudflareAccountResponseAttributes
    from datadog_api_client.v2.model.cloudflare_account_type import CloudflareAccountType


class CloudflareAccountResponseData(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.cloudflare_account_response_attributes import (
            CloudflareAccountResponseAttributes,
        )
        from datadog_api_client.v2.model.cloudflare_account_type import CloudflareAccountType

        return {
            "attributes": (CloudflareAccountResponseAttributes,),
            "id": (str,),
            "type": (CloudflareAccountType,),
        }

    attribute_map = {
        "attributes": "attributes",
        "id": "id",
        "type": "type",
    }

    def __init__(
        self_, attributes: CloudflareAccountResponseAttributes, id: str, type: CloudflareAccountType, **kwargs
    ):
        """
        Data object of a Cloudflare account.

        :param attributes: Attributes object of a Cloudflare account.
        :type attributes: CloudflareAccountResponseAttributes

        :param id: The ID of the Cloudflare account, a hash of the account name.
        :type id: str

        :param type: The JSON:API type for this API. Should always be ``cloudflare-accounts``.
        :type type: CloudflareAccountType
        """
        super().__init__(kwargs)

        self_.attributes = attributes
        self_.id = id
        self_.type = type
