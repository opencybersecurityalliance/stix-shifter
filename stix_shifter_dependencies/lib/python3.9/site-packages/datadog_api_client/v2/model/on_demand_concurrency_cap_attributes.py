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


class OnDemandConcurrencyCapAttributes(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "on_demand_concurrency_cap": (float,),
        }

    attribute_map = {
        "on_demand_concurrency_cap": "on_demand_concurrency_cap",
    }

    def __init__(self_, on_demand_concurrency_cap: Union[float, UnsetType] = unset, **kwargs):
        """
        On-demand concurrency cap attributes.

        :param on_demand_concurrency_cap: Value of the on-demand concurrency cap.
        :type on_demand_concurrency_cap: float, optional
        """
        if on_demand_concurrency_cap is not unset:
            kwargs["on_demand_concurrency_cap"] = on_demand_concurrency_cap
        super().__init__(kwargs)
