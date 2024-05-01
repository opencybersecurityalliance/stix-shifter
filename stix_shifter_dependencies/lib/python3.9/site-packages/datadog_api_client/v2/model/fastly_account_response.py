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
    from datadog_api_client.v2.model.fastly_account_response_data import FastlyAccountResponseData


class FastlyAccountResponse(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.fastly_account_response_data import FastlyAccountResponseData

        return {
            "data": (FastlyAccountResponseData,),
        }

    attribute_map = {
        "data": "data",
    }

    def __init__(self_, data: Union[FastlyAccountResponseData, UnsetType] = unset, **kwargs):
        """
        The expected response schema when getting a Fastly account.

        :param data: Data object of a Fastly account.
        :type data: FastlyAccountResponseData, optional
        """
        if data is not unset:
            kwargs["data"] = data
        super().__init__(kwargs)
