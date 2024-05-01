# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Union

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    datetime,
    unset,
    UnsetType,
)


class SecurityMonitoringSignalListRequestFilter(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "_from": (datetime,),
            "query": (str,),
            "to": (datetime,),
        }

    attribute_map = {
        "_from": "from",
        "query": "query",
        "to": "to",
    }

    def __init__(
        self_,
        _from: Union[datetime, UnsetType] = unset,
        query: Union[str, UnsetType] = unset,
        to: Union[datetime, UnsetType] = unset,
        **kwargs,
    ):
        """
        Search filters for listing security signals.

        :param _from: The minimum timestamp for requested security signals.
        :type _from: datetime, optional

        :param query: Search query for listing security signals.
        :type query: str, optional

        :param to: The maximum timestamp for requested security signals.
        :type to: datetime, optional
        """
        if _from is not unset:
            kwargs["_from"] = _from
        if query is not unset:
            kwargs["query"] = query
        if to is not unset:
            kwargs["to"] = to
        super().__init__(kwargs)
