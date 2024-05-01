# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import List, Union, TYPE_CHECKING

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    unset,
    UnsetType,
)


if TYPE_CHECKING:
    from datadog_api_client.v1.model.synthetics_test_options_scheduling_timeframe import (
        SyntheticsTestOptionsSchedulingTimeframe,
    )


class SyntheticsTestOptionsScheduling(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.synthetics_test_options_scheduling_timeframe import (
            SyntheticsTestOptionsSchedulingTimeframe,
        )

        return {
            "timeframes": ([SyntheticsTestOptionsSchedulingTimeframe],),
            "timezone": (str,),
        }

    attribute_map = {
        "timeframes": "timeframes",
        "timezone": "timezone",
    }

    def __init__(
        self_,
        timeframes: Union[List[SyntheticsTestOptionsSchedulingTimeframe], UnsetType] = unset,
        timezone: Union[str, UnsetType] = unset,
        **kwargs,
    ):
        """
        Object containing timeframes and timezone used for advanced scheduling.

        :param timeframes: Array containing objects describing the scheduling pattern to apply to each day.
        :type timeframes: [SyntheticsTestOptionsSchedulingTimeframe], optional

        :param timezone: Timezone in which the timeframe is based.
        :type timezone: str, optional
        """
        if timeframes is not unset:
            kwargs["timeframes"] = timeframes
        if timezone is not unset:
            kwargs["timezone"] = timezone
        super().__init__(kwargs)
