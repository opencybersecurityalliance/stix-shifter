# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import List, TYPE_CHECKING

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
)


if TYPE_CHECKING:
    from datadog_api_client.v2.model.security_filter_exclusion_filter import SecurityFilterExclusionFilter
    from datadog_api_client.v2.model.security_filter_filtered_data_type import SecurityFilterFilteredDataType


class SecurityFilterCreateAttributes(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.security_filter_exclusion_filter import SecurityFilterExclusionFilter
        from datadog_api_client.v2.model.security_filter_filtered_data_type import SecurityFilterFilteredDataType

        return {
            "exclusion_filters": ([SecurityFilterExclusionFilter],),
            "filtered_data_type": (SecurityFilterFilteredDataType,),
            "is_enabled": (bool,),
            "name": (str,),
            "query": (str,),
        }

    attribute_map = {
        "exclusion_filters": "exclusion_filters",
        "filtered_data_type": "filtered_data_type",
        "is_enabled": "is_enabled",
        "name": "name",
        "query": "query",
    }

    def __init__(
        self_,
        exclusion_filters: List[SecurityFilterExclusionFilter],
        filtered_data_type: SecurityFilterFilteredDataType,
        is_enabled: bool,
        name: str,
        query: str,
        **kwargs,
    ):
        """
        Object containing the attributes of the security filter to be created.

        :param exclusion_filters: Exclusion filters to exclude some logs from the security filter.
        :type exclusion_filters: [SecurityFilterExclusionFilter]

        :param filtered_data_type: The filtered data type.
        :type filtered_data_type: SecurityFilterFilteredDataType

        :param is_enabled: Whether the security filter is enabled.
        :type is_enabled: bool

        :param name: The name of the security filter.
        :type name: str

        :param query: The query of the security filter.
        :type query: str
        """
        super().__init__(kwargs)

        self_.exclusion_filters = exclusion_filters
        self_.filtered_data_type = filtered_data_type
        self_.is_enabled = is_enabled
        self_.name = name
        self_.query = query
