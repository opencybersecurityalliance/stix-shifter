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
    from datadog_api_client.v1.model.synthetics_api_test_result_short_result import SyntheticsAPITestResultShortResult
    from datadog_api_client.v1.model.synthetics_test_monitor_status import SyntheticsTestMonitorStatus


class SyntheticsAPITestResultShort(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.synthetics_api_test_result_short_result import (
            SyntheticsAPITestResultShortResult,
        )
        from datadog_api_client.v1.model.synthetics_test_monitor_status import SyntheticsTestMonitorStatus

        return {
            "check_time": (float,),
            "probe_dc": (str,),
            "result": (SyntheticsAPITestResultShortResult,),
            "result_id": (str,),
            "status": (SyntheticsTestMonitorStatus,),
        }

    attribute_map = {
        "check_time": "check_time",
        "probe_dc": "probe_dc",
        "result": "result",
        "result_id": "result_id",
        "status": "status",
    }

    def __init__(
        self_,
        check_time: Union[float, UnsetType] = unset,
        probe_dc: Union[str, UnsetType] = unset,
        result: Union[SyntheticsAPITestResultShortResult, UnsetType] = unset,
        result_id: Union[str, UnsetType] = unset,
        status: Union[SyntheticsTestMonitorStatus, UnsetType] = unset,
        **kwargs,
    ):
        """
        Object with the results of a single Synthetic API test.

        :param check_time: Last time the API test was performed.
        :type check_time: float, optional

        :param probe_dc: Location from which the API test was performed.
        :type probe_dc: str, optional

        :param result: Result of the last API test run.
        :type result: SyntheticsAPITestResultShortResult, optional

        :param result_id: ID of the API test result.
        :type result_id: str, optional

        :param status: The status of your Synthetic monitor.

            * ``O`` for not triggered
            * ``1`` for triggered
            * ``2`` for no data
        :type status: SyntheticsTestMonitorStatus, optional
        """
        if check_time is not unset:
            kwargs["check_time"] = check_time
        if probe_dc is not unset:
            kwargs["probe_dc"] = probe_dc
        if result is not unset:
            kwargs["result"] = result
        if result_id is not unset:
            kwargs["result_id"] = result_id
        if status is not unset:
            kwargs["status"] = status
        super().__init__(kwargs)
