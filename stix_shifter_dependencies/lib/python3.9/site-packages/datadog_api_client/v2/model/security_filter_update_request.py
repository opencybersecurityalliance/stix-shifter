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
    from datadog_api_client.v2.model.security_filter_update_data import SecurityFilterUpdateData


class SecurityFilterUpdateRequest(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.security_filter_update_data import SecurityFilterUpdateData

        return {
            "data": (SecurityFilterUpdateData,),
        }

    attribute_map = {
        "data": "data",
    }

    def __init__(self_, data: SecurityFilterUpdateData, **kwargs):
        """
        The new security filter body.

        :param data: The new security filter properties.
        :type data: SecurityFilterUpdateData
        """
        super().__init__(kwargs)

        self_.data = data
