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
    from datadog_api_client.v1.model.synthetics_device import SyntheticsDevice


class SyntheticsBrowserTestResultShortResult(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.synthetics_device import SyntheticsDevice

        return {
            "device": (SyntheticsDevice,),
            "duration": (float,),
            "error_count": (int,),
            "step_count_completed": (int,),
            "step_count_total": (int,),
        }

    attribute_map = {
        "device": "device",
        "duration": "duration",
        "error_count": "errorCount",
        "step_count_completed": "stepCountCompleted",
        "step_count_total": "stepCountTotal",
    }

    def __init__(
        self_,
        device: Union[SyntheticsDevice, UnsetType] = unset,
        duration: Union[float, UnsetType] = unset,
        error_count: Union[int, UnsetType] = unset,
        step_count_completed: Union[int, UnsetType] = unset,
        step_count_total: Union[int, UnsetType] = unset,
        **kwargs,
    ):
        """
        Object with the result of the last browser test run.

        :param device: Object describing the device used to perform the Synthetic test.
        :type device: SyntheticsDevice, optional

        :param duration: Length in milliseconds of the browser test run.
        :type duration: float, optional

        :param error_count: Amount of errors collected for a single browser test run.
        :type error_count: int, optional

        :param step_count_completed: Amount of browser test steps completed before failing.
        :type step_count_completed: int, optional

        :param step_count_total: Total amount of browser test steps.
        :type step_count_total: int, optional
        """
        if device is not unset:
            kwargs["device"] = device
        if duration is not unset:
            kwargs["duration"] = duration
        if error_count is not unset:
            kwargs["error_count"] = error_count
        if step_count_completed is not unset:
            kwargs["step_count_completed"] = step_count_completed
        if step_count_total is not unset:
            kwargs["step_count_total"] = step_count_total
        super().__init__(kwargs)
