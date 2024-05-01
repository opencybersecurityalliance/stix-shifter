# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import List, Union, TYPE_CHECKING

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    none_type,
    unset,
    UnsetType,
)


if TYPE_CHECKING:
    from datadog_api_client.v1.model.slo_error_budget_remaining_data import SLOErrorBudgetRemainingData
    from datadog_api_client.v1.model.slo_history_response_error_with_type import SLOHistoryResponseErrorWithType


class SLOHistoryMonitor(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.slo_error_budget_remaining_data import SLOErrorBudgetRemainingData
        from datadog_api_client.v1.model.slo_history_response_error_with_type import SLOHistoryResponseErrorWithType

        return {
            "error_budget_remaining": (SLOErrorBudgetRemainingData,),
            "errors": ([SLOHistoryResponseErrorWithType],),
            "group": (str,),
            "history": ([[float]],),
            "monitor_modified": (int,),
            "monitor_type": (str,),
            "name": (str,),
            "precision": (float,),
            "preview": (bool,),
            "sli_value": (float, none_type),
            "span_precision": (float,),
            "uptime": (float,),
        }

    attribute_map = {
        "error_budget_remaining": "error_budget_remaining",
        "errors": "errors",
        "group": "group",
        "history": "history",
        "monitor_modified": "monitor_modified",
        "monitor_type": "monitor_type",
        "name": "name",
        "precision": "precision",
        "preview": "preview",
        "sli_value": "sli_value",
        "span_precision": "span_precision",
        "uptime": "uptime",
    }

    def __init__(
        self_,
        error_budget_remaining: Union[SLOErrorBudgetRemainingData, UnsetType] = unset,
        errors: Union[List[SLOHistoryResponseErrorWithType], UnsetType] = unset,
        group: Union[str, UnsetType] = unset,
        history: Union[List[List[float]], UnsetType] = unset,
        monitor_modified: Union[int, UnsetType] = unset,
        monitor_type: Union[str, UnsetType] = unset,
        name: Union[str, UnsetType] = unset,
        precision: Union[float, UnsetType] = unset,
        preview: Union[bool, UnsetType] = unset,
        sli_value: Union[float, none_type, UnsetType] = unset,
        span_precision: Union[float, UnsetType] = unset,
        uptime: Union[float, UnsetType] = unset,
        **kwargs,
    ):
        """
        An object that holds an SLI value and its associated data. It can represent an SLO's overall SLI value.
        This can also represent the SLI value for a specific monitor in multi-monitor SLOs, or a group in grouped SLOs.

        :param error_budget_remaining: A mapping of threshold ``timeframe`` to the remaining error budget.
        :type error_budget_remaining: SLOErrorBudgetRemainingData, optional

        :param errors: An array of error objects returned while querying the history data for the service level objective.
        :type errors: [SLOHistoryResponseErrorWithType], optional

        :param group: For groups in a grouped SLO, this is the group name.
        :type group: str, optional

        :param history: For ``monitor`` based SLOs, this includes the aggregated history as arrays that include time series and uptime data where ``0=monitor`` is in ``OK`` state and ``1=monitor`` is in ``alert`` state.
        :type history: [[float]], optional

        :param monitor_modified: For ``monitor`` based SLOs, this is the last modified timestamp in epoch seconds of the monitor.
        :type monitor_modified: int, optional

        :param monitor_type: For ``monitor`` based SLOs, this describes the type of monitor.
        :type monitor_type: str, optional

        :param name: For groups in a grouped SLO, this is the group name. For monitors in a multi-monitor SLO, this is the monitor name.
        :type name: str, optional

        :param precision: The amount of decimal places the SLI value is accurate to for the given from ``&&`` to timestamp. Use ``span_precision`` instead. **Deprecated**.
        :type precision: float, optional

        :param preview: For ``monitor`` based SLOs, when ``true`` this indicates that a replay is in progress to give an accurate uptime
            calculation.
        :type preview: bool, optional

        :param sli_value: The current SLI value of the SLO over the history window.
        :type sli_value: float, none_type, optional

        :param span_precision: The amount of decimal places the SLI value is accurate to for the given from ``&&`` to timestamp.
        :type span_precision: float, optional

        :param uptime: Use ``sli_value`` instead. **Deprecated**.
        :type uptime: float, optional
        """
        if error_budget_remaining is not unset:
            kwargs["error_budget_remaining"] = error_budget_remaining
        if errors is not unset:
            kwargs["errors"] = errors
        if group is not unset:
            kwargs["group"] = group
        if history is not unset:
            kwargs["history"] = history
        if monitor_modified is not unset:
            kwargs["monitor_modified"] = monitor_modified
        if monitor_type is not unset:
            kwargs["monitor_type"] = monitor_type
        if name is not unset:
            kwargs["name"] = name
        if precision is not unset:
            kwargs["precision"] = precision
        if preview is not unset:
            kwargs["preview"] = preview
        if sli_value is not unset:
            kwargs["sli_value"] = sli_value
        if span_precision is not unset:
            kwargs["span_precision"] = span_precision
        if uptime is not unset:
            kwargs["uptime"] = uptime
        super().__init__(kwargs)
