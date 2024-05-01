# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Any, List, Union, TYPE_CHECKING

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    date,
    datetime,
    none_type,
    unset,
    UnsetType,
)


if TYPE_CHECKING:
    from datadog_api_client.v1.model.synthetics_browser_error import SyntheticsBrowserError
    from datadog_api_client.v1.model.synthetics_check_type import SyntheticsCheckType
    from datadog_api_client.v1.model.synthetics_playing_tab import SyntheticsPlayingTab
    from datadog_api_client.v1.model.synthetics_step_type import SyntheticsStepType
    from datadog_api_client.v1.model.synthetics_core_web_vitals import SyntheticsCoreWebVitals
    from datadog_api_client.v1.model.synthetics_step_detail_warning import SyntheticsStepDetailWarning


class SyntheticsStepDetail(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.synthetics_browser_error import SyntheticsBrowserError
        from datadog_api_client.v1.model.synthetics_check_type import SyntheticsCheckType
        from datadog_api_client.v1.model.synthetics_playing_tab import SyntheticsPlayingTab
        from datadog_api_client.v1.model.synthetics_step_type import SyntheticsStepType
        from datadog_api_client.v1.model.synthetics_core_web_vitals import SyntheticsCoreWebVitals
        from datadog_api_client.v1.model.synthetics_step_detail_warning import SyntheticsStepDetailWarning

        return {
            "browser_errors": ([SyntheticsBrowserError],),
            "check_type": (SyntheticsCheckType,),
            "description": (str,),
            "duration": (float,),
            "error": (str,),
            "playing_tab": (SyntheticsPlayingTab,),
            "screenshot_bucket_key": (bool,),
            "skipped": (bool,),
            "snapshot_bucket_key": (bool,),
            "step_id": (int,),
            "sub_test_step_details": ([SyntheticsStepDetail],),
            "time_to_interactive": (float,),
            "type": (SyntheticsStepType,),
            "url": (str,),
            "value": (
                bool,
                date,
                datetime,
                dict,
                float,
                int,
                list,
                str,
                none_type,
            ),
            "vitals_metrics": ([SyntheticsCoreWebVitals],),
            "warnings": ([SyntheticsStepDetailWarning],),
        }

    attribute_map = {
        "browser_errors": "browserErrors",
        "check_type": "checkType",
        "description": "description",
        "duration": "duration",
        "error": "error",
        "playing_tab": "playingTab",
        "screenshot_bucket_key": "screenshotBucketKey",
        "skipped": "skipped",
        "snapshot_bucket_key": "snapshotBucketKey",
        "step_id": "stepId",
        "sub_test_step_details": "subTestStepDetails",
        "time_to_interactive": "timeToInteractive",
        "type": "type",
        "url": "url",
        "value": "value",
        "vitals_metrics": "vitalsMetrics",
        "warnings": "warnings",
    }

    def __init__(
        self_,
        browser_errors: Union[List[SyntheticsBrowserError], UnsetType] = unset,
        check_type: Union[SyntheticsCheckType, UnsetType] = unset,
        description: Union[str, UnsetType] = unset,
        duration: Union[float, UnsetType] = unset,
        error: Union[str, UnsetType] = unset,
        playing_tab: Union[SyntheticsPlayingTab, UnsetType] = unset,
        screenshot_bucket_key: Union[bool, UnsetType] = unset,
        skipped: Union[bool, UnsetType] = unset,
        snapshot_bucket_key: Union[bool, UnsetType] = unset,
        step_id: Union[int, UnsetType] = unset,
        sub_test_step_details: Union[List[SyntheticsStepDetail], UnsetType] = unset,
        time_to_interactive: Union[float, UnsetType] = unset,
        type: Union[SyntheticsStepType, UnsetType] = unset,
        url: Union[str, UnsetType] = unset,
        value: Union[Any, UnsetType] = unset,
        vitals_metrics: Union[List[SyntheticsCoreWebVitals], UnsetType] = unset,
        warnings: Union[List[SyntheticsStepDetailWarning], UnsetType] = unset,
        **kwargs,
    ):
        """
        Object describing a step for a Synthetic test.

        :param browser_errors: Array of errors collected for a browser test.
        :type browser_errors: [SyntheticsBrowserError], optional

        :param check_type: Type of assertion to apply in an API test.
        :type check_type: SyntheticsCheckType, optional

        :param description: Description of the test.
        :type description: str, optional

        :param duration: Total duration in millisecond of the test.
        :type duration: float, optional

        :param error: Error returned by the test.
        :type error: str, optional

        :param playing_tab: Navigate between different tabs for your browser test.
        :type playing_tab: SyntheticsPlayingTab, optional

        :param screenshot_bucket_key: Whether or not screenshots where collected by the test.
        :type screenshot_bucket_key: bool, optional

        :param skipped: Whether or not to skip this step.
        :type skipped: bool, optional

        :param snapshot_bucket_key: Whether or not snapshots where collected by the test.
        :type snapshot_bucket_key: bool, optional

        :param step_id: The step ID.
        :type step_id: int, optional

        :param sub_test_step_details: If this steps include a sub-test.
            `Subtests documentation <https://docs.datadoghq.com/synthetics/browser_tests/advanced_options/#subtests>`_.
        :type sub_test_step_details: [SyntheticsStepDetail], optional

        :param time_to_interactive: Time before starting the step.
        :type time_to_interactive: float, optional

        :param type: Step type used in your Synthetic test.
        :type type: SyntheticsStepType, optional

        :param url: URL to perform the step against.
        :type url: str, optional

        :param value: Value for the step.
        :type value: bool, date, datetime, dict, float, int, list, str, none_type, optional

        :param vitals_metrics: Array of Core Web Vitals metrics for the step.
        :type vitals_metrics: [SyntheticsCoreWebVitals], optional

        :param warnings: Warning collected that didn't failed the step.
        :type warnings: [SyntheticsStepDetailWarning], optional
        """
        if browser_errors is not unset:
            kwargs["browser_errors"] = browser_errors
        if check_type is not unset:
            kwargs["check_type"] = check_type
        if description is not unset:
            kwargs["description"] = description
        if duration is not unset:
            kwargs["duration"] = duration
        if error is not unset:
            kwargs["error"] = error
        if playing_tab is not unset:
            kwargs["playing_tab"] = playing_tab
        if screenshot_bucket_key is not unset:
            kwargs["screenshot_bucket_key"] = screenshot_bucket_key
        if skipped is not unset:
            kwargs["skipped"] = skipped
        if snapshot_bucket_key is not unset:
            kwargs["snapshot_bucket_key"] = snapshot_bucket_key
        if step_id is not unset:
            kwargs["step_id"] = step_id
        if sub_test_step_details is not unset:
            kwargs["sub_test_step_details"] = sub_test_step_details
        if time_to_interactive is not unset:
            kwargs["time_to_interactive"] = time_to_interactive
        if type is not unset:
            kwargs["type"] = type
        if url is not unset:
            kwargs["url"] = url
        if value is not unset:
            kwargs["value"] = value
        if vitals_metrics is not unset:
            kwargs["vitals_metrics"] = vitals_metrics
        if warnings is not unset:
            kwargs["warnings"] = warnings
        super().__init__(kwargs)
