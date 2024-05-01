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
    from datadog_api_client.v1.model.synthetics_device_id import SyntheticsDeviceID
    from datadog_api_client.v1.model.synthetics_test_execution_rule import SyntheticsTestExecutionRule
    from datadog_api_client.v1.model.synthetics_status import SyntheticsStatus
    from datadog_api_client.v1.model.synthetics_test_details_type import SyntheticsTestDetailsType


class SyntheticsBatchResult(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.synthetics_device_id import SyntheticsDeviceID
        from datadog_api_client.v1.model.synthetics_test_execution_rule import SyntheticsTestExecutionRule
        from datadog_api_client.v1.model.synthetics_status import SyntheticsStatus
        from datadog_api_client.v1.model.synthetics_test_details_type import SyntheticsTestDetailsType

        return {
            "device": (SyntheticsDeviceID,),
            "duration": (float,),
            "execution_rule": (SyntheticsTestExecutionRule,),
            "location": (str,),
            "result_id": (str,),
            "retries": (float,),
            "status": (SyntheticsStatus,),
            "test_name": (str,),
            "test_public_id": (str,),
            "test_type": (SyntheticsTestDetailsType,),
        }

    attribute_map = {
        "device": "device",
        "duration": "duration",
        "execution_rule": "execution_rule",
        "location": "location",
        "result_id": "result_id",
        "retries": "retries",
        "status": "status",
        "test_name": "test_name",
        "test_public_id": "test_public_id",
        "test_type": "test_type",
    }

    def __init__(
        self_,
        device: Union[SyntheticsDeviceID, UnsetType] = unset,
        duration: Union[float, UnsetType] = unset,
        execution_rule: Union[SyntheticsTestExecutionRule, UnsetType] = unset,
        location: Union[str, UnsetType] = unset,
        result_id: Union[str, UnsetType] = unset,
        retries: Union[float, UnsetType] = unset,
        status: Union[SyntheticsStatus, UnsetType] = unset,
        test_name: Union[str, UnsetType] = unset,
        test_public_id: Union[str, UnsetType] = unset,
        test_type: Union[SyntheticsTestDetailsType, UnsetType] = unset,
        **kwargs,
    ):
        """
        Object with the results of a Synthetics batch.

        :param device: The device ID.
        :type device: SyntheticsDeviceID, optional

        :param duration: Total duration in millisecond of the test.
        :type duration: float, optional

        :param execution_rule: Execution rule for a Synthetics test.
        :type execution_rule: SyntheticsTestExecutionRule, optional

        :param location: Name of the location.
        :type location: str, optional

        :param result_id: The ID of the result to get.
        :type result_id: str, optional

        :param retries: Number of times this result has been retried.
        :type retries: float, optional

        :param status: Determines whether or not the batch has passed, failed, or is in progress.
        :type status: SyntheticsStatus, optional

        :param test_name: Name of the test.
        :type test_name: str, optional

        :param test_public_id: The public ID of the Synthetic test.
        :type test_public_id: str, optional

        :param test_type: Type of the Synthetic test, either ``api`` or ``browser``.
        :type test_type: SyntheticsTestDetailsType, optional
        """
        if device is not unset:
            kwargs["device"] = device
        if duration is not unset:
            kwargs["duration"] = duration
        if execution_rule is not unset:
            kwargs["execution_rule"] = execution_rule
        if location is not unset:
            kwargs["location"] = location
        if result_id is not unset:
            kwargs["result_id"] = result_id
        if retries is not unset:
            kwargs["retries"] = retries
        if status is not unset:
            kwargs["status"] = status
        if test_name is not unset:
            kwargs["test_name"] = test_name
        if test_public_id is not unset:
            kwargs["test_public_id"] = test_public_id
        if test_type is not unset:
            kwargs["test_type"] = test_type
        super().__init__(kwargs)
