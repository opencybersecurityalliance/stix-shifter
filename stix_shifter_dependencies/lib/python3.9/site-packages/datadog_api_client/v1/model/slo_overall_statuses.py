# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Union, TYPE_CHECKING

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    none_type,
    unset,
    UnsetType,
)


if TYPE_CHECKING:
    from datadog_api_client.v1.model.slo_raw_error_budget_remaining import SLORawErrorBudgetRemaining
    from datadog_api_client.v1.model.slo_state import SLOState
    from datadog_api_client.v1.model.slo_timeframe import SLOTimeframe


class SLOOverallStatuses(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.slo_raw_error_budget_remaining import SLORawErrorBudgetRemaining
        from datadog_api_client.v1.model.slo_state import SLOState
        from datadog_api_client.v1.model.slo_timeframe import SLOTimeframe

        return {
            "error": (str, none_type),
            "error_budget_remaining": (float, none_type),
            "indexed_at": (int,),
            "raw_error_budget_remaining": (SLORawErrorBudgetRemaining,),
            "span_precision": (int, none_type),
            "state": (SLOState,),
            "status": (float, none_type),
            "target": (float,),
            "timeframe": (SLOTimeframe,),
        }

    attribute_map = {
        "error": "error",
        "error_budget_remaining": "error_budget_remaining",
        "indexed_at": "indexed_at",
        "raw_error_budget_remaining": "raw_error_budget_remaining",
        "span_precision": "span_precision",
        "state": "state",
        "status": "status",
        "target": "target",
        "timeframe": "timeframe",
    }

    def __init__(
        self_,
        error: Union[str, none_type, UnsetType] = unset,
        error_budget_remaining: Union[float, none_type, UnsetType] = unset,
        indexed_at: Union[int, UnsetType] = unset,
        raw_error_budget_remaining: Union[SLORawErrorBudgetRemaining, none_type, UnsetType] = unset,
        span_precision: Union[int, none_type, UnsetType] = unset,
        state: Union[SLOState, UnsetType] = unset,
        status: Union[float, none_type, UnsetType] = unset,
        target: Union[float, UnsetType] = unset,
        timeframe: Union[SLOTimeframe, UnsetType] = unset,
        **kwargs,
    ):
        """
        Overall status of the SLO by timeframes.

        :param error: Error message if SLO status or error budget could not be calculated.
        :type error: str, none_type, optional

        :param error_budget_remaining: Remaining error budget of the SLO in percentage.
        :type error_budget_remaining: float, none_type, optional

        :param indexed_at: timestamp (UNIX time in seconds) of when the SLO status and error budget
            were calculated.
        :type indexed_at: int, optional

        :param raw_error_budget_remaining: Error budget remaining for an SLO.
        :type raw_error_budget_remaining: SLORawErrorBudgetRemaining, none_type, optional

        :param span_precision: The amount of decimal places the SLI value is accurate to.
        :type span_precision: int, none_type, optional

        :param state: State of the SLO.
        :type state: SLOState, optional

        :param status: The status of the SLO.
        :type status: float, none_type, optional

        :param target: The target of the SLO.
        :type target: float, optional

        :param timeframe: The SLO time window options.
        :type timeframe: SLOTimeframe, optional
        """
        if error is not unset:
            kwargs["error"] = error
        if error_budget_remaining is not unset:
            kwargs["error_budget_remaining"] = error_budget_remaining
        if indexed_at is not unset:
            kwargs["indexed_at"] = indexed_at
        if raw_error_budget_remaining is not unset:
            kwargs["raw_error_budget_remaining"] = raw_error_budget_remaining
        if span_precision is not unset:
            kwargs["span_precision"] = span_precision
        if state is not unset:
            kwargs["state"] = state
        if status is not unset:
            kwargs["status"] = status
        if target is not unset:
            kwargs["target"] = target
        if timeframe is not unset:
            kwargs["timeframe"] = timeframe
        super().__init__(kwargs)
