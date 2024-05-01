# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import List, Union

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    unset,
    UnsetType,
)


class MetricSearchResponseResults(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "metrics": ([str],),
        }

    attribute_map = {
        "metrics": "metrics",
    }

    def __init__(self_, metrics: Union[List[str], UnsetType] = unset, **kwargs):
        """
        Search result.

        :param metrics: List of metrics that match the search query.
        :type metrics: [str], optional
        """
        if metrics is not unset:
            kwargs["metrics"] = metrics
        super().__init__(kwargs)
