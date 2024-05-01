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
    from datadog_api_client.v2.model.security_filter_create_attributes import SecurityFilterCreateAttributes
    from datadog_api_client.v2.model.security_filter_type import SecurityFilterType


class SecurityFilterCreateData(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.security_filter_create_attributes import SecurityFilterCreateAttributes
        from datadog_api_client.v2.model.security_filter_type import SecurityFilterType

        return {
            "attributes": (SecurityFilterCreateAttributes,),
            "type": (SecurityFilterType,),
        }

    attribute_map = {
        "attributes": "attributes",
        "type": "type",
    }

    def __init__(self_, attributes: SecurityFilterCreateAttributes, type: SecurityFilterType, **kwargs):
        """
        Object for a single security filter.

        :param attributes: Object containing the attributes of the security filter to be created.
        :type attributes: SecurityFilterCreateAttributes

        :param type: The type of the resource. The value should always be ``security_filters``.
        :type type: SecurityFilterType
        """
        super().__init__(kwargs)

        self_.attributes = attributes
        self_.type = type
