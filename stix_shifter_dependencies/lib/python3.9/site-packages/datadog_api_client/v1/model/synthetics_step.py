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
    from datadog_api_client.v1.model.synthetics_step_type import SyntheticsStepType


class SyntheticsStep(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.synthetics_step_type import SyntheticsStepType

        return {
            "allow_failure": (bool,),
            "is_critical": (bool,),
            "name": (str,),
            "no_screenshot": (bool,),
            "params": (dict,),
            "timeout": (int,),
            "type": (SyntheticsStepType,),
        }

    attribute_map = {
        "allow_failure": "allowFailure",
        "is_critical": "isCritical",
        "name": "name",
        "no_screenshot": "noScreenshot",
        "params": "params",
        "timeout": "timeout",
        "type": "type",
    }

    def __init__(
        self_,
        allow_failure: Union[bool, UnsetType] = unset,
        is_critical: Union[bool, UnsetType] = unset,
        name: Union[str, UnsetType] = unset,
        no_screenshot: Union[bool, UnsetType] = unset,
        params: Union[dict, UnsetType] = unset,
        timeout: Union[int, UnsetType] = unset,
        type: Union[SyntheticsStepType, UnsetType] = unset,
        **kwargs,
    ):
        """
        The steps used in a Synthetics browser test.

        :param allow_failure: A boolean set to allow this step to fail.
        :type allow_failure: bool, optional

        :param is_critical: A boolean to use in addition to ``allowFailure`` to determine if the test should be marked as failed when the step fails.
        :type is_critical: bool, optional

        :param name: The name of the step.
        :type name: str, optional

        :param no_screenshot: A boolean set to not take a screenshot for the step.
        :type no_screenshot: bool, optional

        :param params: The parameters of the step.
        :type params: dict, optional

        :param timeout: The time before declaring a step failed.
        :type timeout: int, optional

        :param type: Step type used in your Synthetic test.
        :type type: SyntheticsStepType, optional
        """
        if allow_failure is not unset:
            kwargs["allow_failure"] = allow_failure
        if is_critical is not unset:
            kwargs["is_critical"] = is_critical
        if name is not unset:
            kwargs["name"] = name
        if no_screenshot is not unset:
            kwargs["no_screenshot"] = no_screenshot
        if params is not unset:
            kwargs["params"] = params
        if timeout is not unset:
            kwargs["timeout"] = timeout
        if type is not unset:
            kwargs["type"] = type
        super().__init__(kwargs)
