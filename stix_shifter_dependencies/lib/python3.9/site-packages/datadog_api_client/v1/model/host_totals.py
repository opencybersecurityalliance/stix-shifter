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


class HostTotals(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "total_active": (int,),
            "total_up": (int,),
        }

    attribute_map = {
        "total_active": "total_active",
        "total_up": "total_up",
    }

    def __init__(self_, total_active: Union[int, UnsetType] = unset, total_up: Union[int, UnsetType] = unset, **kwargs):
        """
        Total number of host currently monitored by Datadog.

        :param total_active: Total number of active host (UP and ???) reporting to Datadog.
        :type total_active: int, optional

        :param total_up: Number of host that are UP and reporting to Datadog.
        :type total_up: int, optional
        """
        if total_active is not unset:
            kwargs["total_active"] = total_active
        if total_up is not unset:
            kwargs["total_up"] = total_up
        super().__init__(kwargs)
