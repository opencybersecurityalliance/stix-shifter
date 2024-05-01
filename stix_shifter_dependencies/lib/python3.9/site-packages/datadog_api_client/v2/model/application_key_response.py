# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import List, Union, TYPE_CHECKING

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    unset,
    UnsetType,
)


if TYPE_CHECKING:
    from datadog_api_client.v2.model.full_application_key import FullApplicationKey
    from datadog_api_client.v2.model.application_key_response_included_item import ApplicationKeyResponseIncludedItem
    from datadog_api_client.v2.model.user import User
    from datadog_api_client.v2.model.role import Role


class ApplicationKeyResponse(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.full_application_key import FullApplicationKey
        from datadog_api_client.v2.model.application_key_response_included_item import (
            ApplicationKeyResponseIncludedItem,
        )

        return {
            "data": (FullApplicationKey,),
            "included": ([ApplicationKeyResponseIncludedItem],),
        }

    attribute_map = {
        "data": "data",
        "included": "included",
    }

    def __init__(
        self_,
        data: Union[FullApplicationKey, UnsetType] = unset,
        included: Union[List[Union[ApplicationKeyResponseIncludedItem, User, Role]], UnsetType] = unset,
        **kwargs,
    ):
        """
        Response for retrieving an application key.

        :param data: Datadog application key.
        :type data: FullApplicationKey, optional

        :param included: Array of objects related to the application key.
        :type included: [ApplicationKeyResponseIncludedItem], optional
        """
        if data is not unset:
            kwargs["data"] = data
        if included is not unset:
            kwargs["included"] = included
        super().__init__(kwargs)
