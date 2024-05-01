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


class AuditLogsQueryFilter(ModelNormal):
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
        Search and filter query settings.

        :param _from: Minimum time for the requested events. Supports date, math, and regular timestamps (in milliseconds).
        :type _from: str, optional

        :param query: Search query following the Audit Logs search syntax.
        :type query: str, optional

        :param to: Maximum time for the requested events. Supports date, math, and regular timestamps (in milliseconds).
        :type to: str, optional
        """
        if _from is not unset:
            kwargs["_from"] = _from
        if query is not unset:
            kwargs["query"] = query
        if to is not unset:
            kwargs["to"] = to
        super().__init__(kwargs)
