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


class LogsMetricResponseFilter(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "query": (str,),
        }

    attribute_map = {
        "query": "query",
    }

    def __init__(self_, query: Union[str, UnsetType] = unset, **kwargs):
        """
        The log-based metric filter. Logs matching this filter will be aggregated in this metric.

        :param query: The search query - following the log search syntax.
        :type query: str, optional
        """
        if query is not unset:
            kwargs["query"] = query
        super().__init__(kwargs)
