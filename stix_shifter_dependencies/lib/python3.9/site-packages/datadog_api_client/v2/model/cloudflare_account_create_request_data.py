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
    from datadog_api_client.v2.model.cloudflare_account_create_request_attributes import (
        CloudflareAccountCreateRequestAttributes,
    )
    from datadog_api_client.v2.model.cloudflare_account_type import CloudflareAccountType


class CloudflareAccountCreateRequestData(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.cloudflare_account_create_request_attributes import (
            CloudflareAccountCreateRequestAttributes,
        )
        from datadog_api_client.v2.model.cloudflare_account_type import CloudflareAccountType

        return {
            "attributes": (CloudflareAccountCreateRequestAttributes,),
            "type": (CloudflareAccountType,),
        }

    attribute_map = {
        "attributes": "attributes",
        "type": "type",
    }

    def __init__(self_, attributes: CloudflareAccountCreateRequestAttributes, type: CloudflareAccountType, **kwargs):
        """
        Data object for creating a Cloudflare account.

        :param attributes: Attributes object for creating a Cloudflare account.
        :type attributes: CloudflareAccountCreateRequestAttributes

        :param type: The JSON:API type for this API. Should always be ``cloudflare-accounts``.
        :type type: CloudflareAccountType
        """
        super().__init__(kwargs)

        self_.attributes = attributes
        self_.type = type
