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
    from datadog_api_client.v1.model.synthetics_device import SyntheticsDevice
    from datadog_api_client.v1.model.synthetics_browser_test_result_failure import SyntheticsBrowserTestResultFailure
    from datadog_api_client.v1.model.synthetics_step_detail import SyntheticsStepDetail


class SyntheticsBrowserTestResultData(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.synthetics_device import SyntheticsDevice
        from datadog_api_client.v1.model.synthetics_browser_test_result_failure import (
            SyntheticsBrowserTestResultFailure,
        )
        from datadog_api_client.v1.model.synthetics_step_detail import SyntheticsStepDetail

        return {
            "browser_type": (str,),
            "browser_version": (str,),
            "device": (SyntheticsDevice,),
            "duration": (float,),
            "error": (str,),
            "failure": (SyntheticsBrowserTestResultFailure,),
            "passed": (bool,),
            "received_email_count": (int,),
            "start_url": (str,),
            "step_details": ([SyntheticsStepDetail],),
            "thumbnails_bucket_key": (bool,),
            "time_to_interactive": (float,),
        }

    attribute_map = {
        "browser_type": "browserType",
        "browser_version": "browserVersion",
        "device": "device",
        "duration": "duration",
        "error": "error",
        "failure": "failure",
        "passed": "passed",
        "received_email_count": "receivedEmailCount",
        "start_url": "startUrl",
        "step_details": "stepDetails",
        "thumbnails_bucket_key": "thumbnailsBucketKey",
        "time_to_interactive": "timeToInteractive",
    }

    def __init__(
        self_,
        browser_type: Union[str, UnsetType] = unset,
        browser_version: Union[str, UnsetType] = unset,
        device: Union[SyntheticsDevice, UnsetType] = unset,
        duration: Union[float, UnsetType] = unset,
        error: Union[str, UnsetType] = unset,
        failure: Union[SyntheticsBrowserTestResultFailure, UnsetType] = unset,
        passed: Union[bool, UnsetType] = unset,
        received_email_count: Union[int, UnsetType] = unset,
        start_url: Union[str, UnsetType] = unset,
        step_details: Union[List[SyntheticsStepDetail], UnsetType] = unset,
        thumbnails_bucket_key: Union[bool, UnsetType] = unset,
        time_to_interactive: Union[float, UnsetType] = unset,
        **kwargs,
    ):
        """
        Object containing results for your Synthetic browser test.

        :param browser_type: Type of browser device used for the browser test.
        :type browser_type: str, optional

        :param browser_version: Browser version used for the browser test.
        :type browser_version: str, optional

        :param device: Object describing the device used to perform the Synthetic test.
        :type device: SyntheticsDevice, optional

        :param duration: Global duration in second of the browser test.
        :type duration: float, optional

        :param error: Error returned for the browser test.
        :type error: str, optional

        :param failure: The browser test failure details.
        :type failure: SyntheticsBrowserTestResultFailure, optional

        :param passed: Whether or not the browser test was conducted.
        :type passed: bool, optional

        :param received_email_count: The amount of email received during the browser test.
        :type received_email_count: int, optional

        :param start_url: Starting URL for the browser test.
        :type start_url: str, optional

        :param step_details: Array containing the different browser test steps.
        :type step_details: [SyntheticsStepDetail], optional

        :param thumbnails_bucket_key: Whether or not a thumbnail is associated with the browser test.
        :type thumbnails_bucket_key: bool, optional

        :param time_to_interactive: Time in second to wait before the browser test starts after
            reaching the start URL.
        :type time_to_interactive: float, optional
        """
        if browser_type is not unset:
            kwargs["browser_type"] = browser_type
        if browser_version is not unset:
            kwargs["browser_version"] = browser_version
        if device is not unset:
            kwargs["device"] = device
        if duration is not unset:
            kwargs["duration"] = duration
        if error is not unset:
            kwargs["error"] = error
        if failure is not unset:
            kwargs["failure"] = failure
        if passed is not unset:
            kwargs["passed"] = passed
        if received_email_count is not unset:
            kwargs["received_email_count"] = received_email_count
        if start_url is not unset:
            kwargs["start_url"] = start_url
        if step_details is not unset:
            kwargs["step_details"] = step_details
        if thumbnails_bucket_key is not unset:
            kwargs["thumbnails_bucket_key"] = thumbnails_bucket_key
        if time_to_interactive is not unset:
            kwargs["time_to_interactive"] = time_to_interactive
        super().__init__(kwargs)
