# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
)


class SecurityFilterExclusionFilter(ModelNormal):
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

    def __init__(self_, name: str, query: str, **kwargs):
        """
        Exclusion filter for the security filter.

        :param name: Exclusion filter name.
        :type name: str

        :param query: Exclusion filter query. Logs that match this query are excluded from the security filter.
        :type query: str
        """
        super().__init__(kwargs)

        self_.name = name
        self_.query = query
