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
    from datadog_api_client.v2.model.fastly_account_update_request_attributes import (
        FastlyAccountUpdateRequestAttributes,
    )
    from datadog_api_client.v2.model.fastly_account_type import FastlyAccountType


class FastlyAccountUpdateRequestData(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.fastly_account_update_request_attributes import (
            FastlyAccountUpdateRequestAttributes,
        )
        from datadog_api_client.v2.model.fastly_account_type import FastlyAccountType

        return {
            "attributes": (FastlyAccountUpdateRequestAttributes,),
            "type": (FastlyAccountType,),
        }

    attribute_map = {
        "attributes": "attributes",
        "type": "type",
    }

    def __init__(
        self_,
        attributes: Union[FastlyAccountUpdateRequestAttributes, UnsetType] = unset,
        type: Union[FastlyAccountType, UnsetType] = unset,
        **kwargs,
    ):
        """
        Data object for updating a Fastly account.

        :param attributes: Attributes object for updating a Fastly account.
        :type attributes: FastlyAccountUpdateRequestAttributes, optional

        :param type: The JSON:API type for this API. Should always be ``fastly-accounts``.
        :type type: FastlyAccountType, optional
        """
        if attributes is not unset:
            kwargs["attributes"] = attributes
        if type is not unset:
            kwargs["type"] = type
        super().__init__(kwargs)
