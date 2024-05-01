# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Union

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    unset,
    UnsetType,
)


class Pagination(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "total_count": (int,),
            "total_filtered_count": (int,),
        }

    attribute_map = {
        "total_count": "total_count",
        "total_filtered_count": "total_filtered_count",
    }

    def __init__(
        self_, total_count: Union[int, UnsetType] = unset, total_filtered_count: Union[int, UnsetType] = unset, **kwargs
    ):
        """
        Pagination object.

        :param total_count: Total count.
        :type total_count: int, optional

        :param total_filtered_count: Total count of elements matched by the filter.
        :type total_filtered_count: int, optional
        """
        if total_count is not unset:
            kwargs["total_count"] = total_count
        if total_filtered_count is not unset:
            kwargs["total_filtered_count"] = total_filtered_count
        super().__init__(kwargs)
