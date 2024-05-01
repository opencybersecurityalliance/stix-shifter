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


class SecurityFilterExclusionFilterResponse(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "name": (str,),
            "query": (str,),
        }

    attribute_map = {
        "name": "name",
        "query": "query",
    }

    def __init__(self_, name: Union[str, UnsetType] = unset, query: Union[str, UnsetType] = unset, **kwargs):
        """
        A single exclusion filter.

        :param name: The exclusion filter name.
        :type name: str, optional

        :param query: The exclusion filter query.
        :type query: str, optional
        """
        if name is not unset:
            kwargs["name"] = name
        if query is not unset:
            kwargs["query"] = query
        super().__init__(kwargs)
