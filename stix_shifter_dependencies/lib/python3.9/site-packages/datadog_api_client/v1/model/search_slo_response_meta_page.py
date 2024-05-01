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


class SearchSLOResponseMetaPage(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "first_number": (int,),
            "last_number": (int,),
            "next_number": (int,),
            "number": (int,),
            "prev_number": (int,),
            "size": (int,),
            "total": (int,),
            "type": (str,),
        }

    attribute_map = {
        "first_number": "first_number",
        "last_number": "last_number",
        "next_number": "next_number",
        "number": "number",
        "prev_number": "prev_number",
        "size": "size",
        "total": "total",
        "type": "type",
    }

    def __init__(
        self_,
        first_number: Union[int, UnsetType] = unset,
        last_number: Union[int, UnsetType] = unset,
        next_number: Union[int, UnsetType] = unset,
        number: Union[int, UnsetType] = unset,
        prev_number: Union[int, UnsetType] = unset,
        size: Union[int, UnsetType] = unset,
        total: Union[int, UnsetType] = unset,
        type: Union[str, UnsetType] = unset,
        **kwargs,
    ):
        """
        Pagination metadata returned by the API.

        :param first_number: The first number.
        :type first_number: int, optional

        :param last_number: The last number.
        :type last_number: int, optional

        :param next_number: The next number.
        :type next_number: int, optional

        :param number: The page number.
        :type number: int, optional

        :param prev_number: The previous page number.
        :type prev_number: int, optional

        :param size: The size of the response.
        :type size: int, optional

        :param total: The total number of SLOs in the response.
        :type total: int, optional

        :param type: Type of pagination.
        :type type: str, optional
        """
        if first_number is not unset:
            kwargs["first_number"] = first_number
        if last_number is not unset:
            kwargs["last_number"] = last_number
        if next_number is not unset:
            kwargs["next_number"] = next_number
        if number is not unset:
            kwargs["number"] = number
        if prev_number is not unset:
            kwargs["prev_number"] = prev_number
        if size is not unset:
            kwargs["size"] = size
        if total is not unset:
            kwargs["total"] = total
        if type is not unset:
            kwargs["type"] = type
        super().__init__(kwargs)
