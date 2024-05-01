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
    from datadog_api_client.v2.model.fastly_account_create_request_data import FastlyAccountCreateRequestData


class FastlyAccountCreateRequest(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.fastly_account_create_request_data import FastlyAccountCreateRequestData

        return {
            "data": (FastlyAccountCreateRequestData,),
        }

    attribute_map = {
        "data": "data",
    }

    def __init__(self_, data: FastlyAccountCreateRequestData, **kwargs):
        """
        Payload schema when adding a Fastly account.

        :param data: Data object for creating a Fastly account.
        :type data: FastlyAccountCreateRequestData
        """
        super().__init__(kwargs)

        self_.data = data
