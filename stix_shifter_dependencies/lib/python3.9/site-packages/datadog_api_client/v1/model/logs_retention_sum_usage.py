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


class LogsRetentionSumUsage(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "logs_indexed_logs_usage_sum": (int,),
            "logs_live_indexed_logs_usage_sum": (int,),
            "logs_rehydrated_indexed_logs_usage_sum": (int,),
            "retention": (str,),
        }

    attribute_map = {
        "logs_indexed_logs_usage_sum": "logs_indexed_logs_usage_sum",
        "logs_live_indexed_logs_usage_sum": "logs_live_indexed_logs_usage_sum",
        "logs_rehydrated_indexed_logs_usage_sum": "logs_rehydrated_indexed_logs_usage_sum",
        "retention": "retention",
    }

    def __init__(
        self_,
        logs_indexed_logs_usage_sum: Union[int, UnsetType] = unset,
        logs_live_indexed_logs_usage_sum: Union[int, UnsetType] = unset,
        logs_rehydrated_indexed_logs_usage_sum: Union[int, UnsetType] = unset,
        retention: Union[str, UnsetType] = unset,
        **kwargs,
    ):
        """
        Object containing indexed logs usage grouped by retention period and summed.

        :param logs_indexed_logs_usage_sum: Total indexed logs for this retention period.
        :type logs_indexed_logs_usage_sum: int, optional

        :param logs_live_indexed_logs_usage_sum: Live indexed logs for this retention period.
        :type logs_live_indexed_logs_usage_sum: int, optional

        :param logs_rehydrated_indexed_logs_usage_sum: Rehydrated indexed logs for this retention period.
        :type logs_rehydrated_indexed_logs_usage_sum: int, optional

        :param retention: The retention period in days or "custom" for all custom retention periods.
        :type retention: str, optional
        """
        if logs_indexed_logs_usage_sum is not unset:
            kwargs["logs_indexed_logs_usage_sum"] = logs_indexed_logs_usage_sum
        if logs_live_indexed_logs_usage_sum is not unset:
            kwargs["logs_live_indexed_logs_usage_sum"] = logs_live_indexed_logs_usage_sum
        if logs_rehydrated_indexed_logs_usage_sum is not unset:
            kwargs["logs_rehydrated_indexed_logs_usage_sum"] = logs_rehydrated_indexed_logs_usage_sum
        if retention is not unset:
            kwargs["retention"] = retention
        super().__init__(kwargs)
