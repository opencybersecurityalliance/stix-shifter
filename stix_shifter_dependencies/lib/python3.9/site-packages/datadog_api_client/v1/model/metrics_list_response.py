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


class MetricsListResponse(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "_from": (str,),
            "metrics": ([str],),
        }

    attribute_map = {
        "_from": "from",
        "metrics": "metrics",
    }

    def __init__(self_, _from: Union[str, UnsetType] = unset, metrics: Union[List[str], UnsetType] = unset, **kwargs):
        """
        Object listing all metric names stored by Datadog since a given time.

        :param _from: Time when the metrics were active, seconds since the Unix epoch.
        :type _from: str, optional

        :param metrics: List of metric names.
        :type metrics: [str], optional
        """
        if _from is not unset:
            kwargs["_from"] = _from
        if metrics is not unset:
            kwargs["metrics"] = metrics
        super().__init__(kwargs)
