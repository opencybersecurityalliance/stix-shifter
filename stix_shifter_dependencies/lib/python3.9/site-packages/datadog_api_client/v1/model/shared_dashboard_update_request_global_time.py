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
    from datadog_api_client.v1.model.dashboard_global_time_live_span import DashboardGlobalTimeLiveSpan


class SharedDashboardUpdateRequestGlobalTime(ModelNormal):
    _nullable = True

    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.dashboard_global_time_live_span import DashboardGlobalTimeLiveSpan

        return {
            "live_span": (DashboardGlobalTimeLiveSpan,),
        }

    attribute_map = {
        "live_span": "live_span",
    }

    def __init__(self_, live_span: Union[DashboardGlobalTimeLiveSpan, UnsetType] = unset, **kwargs):
        """
        Timeframe setting for the shared dashboard.

        :param live_span: Dashboard global time live_span selection
        :type live_span: DashboardGlobalTimeLiveSpan, optional
        """
        if live_span is not unset:
            kwargs["live_span"] = live_span
        super().__init__(kwargs)
