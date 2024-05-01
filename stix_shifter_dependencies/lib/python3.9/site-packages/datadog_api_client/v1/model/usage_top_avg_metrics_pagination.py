# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Union

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    none_type,
    unset,
    UnsetType,
)


class UsageTopAvgMetricsPagination(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "limit": (int,),
            "next_record_id": (str, none_type),
            "total_number_of_records": (int, none_type),
        }

    attribute_map = {
        "limit": "limit",
        "next_record_id": "next_record_id",
        "total_number_of_records": "total_number_of_records",
    }

    def __init__(
        self_,
        limit: Union[int, UnsetType] = unset,
        next_record_id: Union[str, none_type, UnsetType] = unset,
        total_number_of_records: Union[int, none_type, UnsetType] = unset,
        **kwargs,
    ):
        """
        The metadata for the current pagination.

        :param limit: Maximum amount of records to be returned.
        :type limit: int, optional

        :param next_record_id: The cursor to get the next results (if any). To make the next request, use the same parameters and add ``next_record_id``.
        :type next_record_id: str, none_type, optional

        :param total_number_of_records: Total number of records.
        :type total_number_of_records: int, none_type, optional
        """
        if limit is not unset:
            kwargs["limit"] = limit
        if next_record_id is not unset:
            kwargs["next_record_id"] = next_record_id
        if total_number_of_records is not unset:
            kwargs["total_number_of_records"] = total_number_of_records
        super().__init__(kwargs)
