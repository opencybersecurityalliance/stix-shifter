# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Union, TYPE_CHECKING

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    unset,
    UnsetType,
)


if TYPE_CHECKING:
    from datadog_api_client.v1.model.monitor_search_count import MonitorSearchCount


class MonitorSearchResponseCounts(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.monitor_search_count import MonitorSearchCount

        return {
            "muted": (MonitorSearchCount,),
            "status": (MonitorSearchCount,),
            "tag": (MonitorSearchCount,),
            "type": (MonitorSearchCount,),
        }

    attribute_map = {
        "muted": "muted",
        "status": "status",
        "tag": "tag",
        "type": "type",
    }

    def __init__(
        self_,
        muted: Union[MonitorSearchCount, UnsetType] = unset,
        status: Union[MonitorSearchCount, UnsetType] = unset,
        tag: Union[MonitorSearchCount, UnsetType] = unset,
        type: Union[MonitorSearchCount, UnsetType] = unset,
        **kwargs,
    ):
        """
        The counts of monitors per different criteria.

        :param muted: Search facets.
        :type muted: MonitorSearchCount, optional

        :param status: Search facets.
        :type status: MonitorSearchCount, optional

        :param tag: Search facets.
        :type tag: MonitorSearchCount, optional

        :param type: Search facets.
        :type type: MonitorSearchCount, optional
        """
        if muted is not unset:
            kwargs["muted"] = muted
        if status is not unset:
            kwargs["status"] = status
        if tag is not unset:
            kwargs["tag"] = tag
        if type is not unset:
            kwargs["type"] = type
        super().__init__(kwargs)
