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


class RUMQueryFilter(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "_from": (str,),
            "query": (str,),
            "to": (str,),
        }

    attribute_map = {
        "_from": "from",
        "query": "query",
        "to": "to",
    }

    def __init__(
        self_,
        _from: Union[str, UnsetType] = unset,
        query: Union[str, UnsetType] = unset,
        to: Union[str, UnsetType] = unset,
        **kwargs,
    ):
        """
        The search and filter query settings.

        :param _from: The minimum time for the requested events; supports date (in `ISO 8601 <https://www.w3.org/TR/NOTE-datetime>`_ format with full date, hours, minutes, and the ``Z`` UTC indicator - seconds and fractional seconds are optional), math, and regular timestamps (in milliseconds).
        :type _from: str, optional

        :param query: The search query following the RUM search syntax.
        :type query: str, optional

        :param to: The maximum time for the requested events; supports date (in `ISO 8601 <https://www.w3.org/TR/NOTE-datetime>`_ format with full date, hours, minutes, and the ``Z`` UTC indicator - seconds and fractional seconds are optional), math, and regular timestamps (in milliseconds).
        :type to: str, optional
        """
        if _from is not unset:
            kwargs["_from"] = _from
        if query is not unset:
            kwargs["query"] = query
        if to is not unset:
            kwargs["to"] = to
        super().__init__(kwargs)
