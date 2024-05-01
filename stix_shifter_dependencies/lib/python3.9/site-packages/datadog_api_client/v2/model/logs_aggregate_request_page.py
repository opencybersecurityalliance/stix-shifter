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


class LogsAggregateRequestPage(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "cursor": (str,),
        }

    attribute_map = {
        "cursor": "cursor",
    }

    def __init__(self_, cursor: Union[str, UnsetType] = unset, **kwargs):
        """
        Paging settings

        :param cursor: The returned paging point to use to get the next results
        :type cursor: str, optional
        """
        if cursor is not unset:
            kwargs["cursor"] = cursor
        super().__init__(kwargs)
