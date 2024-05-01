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
    from datadog_api_client.v1.model.synthetics_timing import SyntheticsTiming


class SyntheticsAPITestResultShortResult(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.synthetics_timing import SyntheticsTiming

        return {
            "passed": (bool,),
            "timings": (SyntheticsTiming,),
        }

    attribute_map = {
        "passed": "passed",
        "timings": "timings",
    }

    def __init__(
        self_, passed: Union[bool, UnsetType] = unset, timings: Union[SyntheticsTiming, UnsetType] = unset, **kwargs
    ):
        """
        Result of the last API test run.

        :param passed: Describes if the test run has passed or failed.
        :type passed: bool, optional

        :param timings: Object containing all metrics and their values collected for a Synthetic API test.
            Learn more about those metrics in `Synthetics documentation <https://docs.datadoghq.com/synthetics/#metrics>`_.
        :type timings: SyntheticsTiming, optional
        """
        if passed is not unset:
            kwargs["passed"] = passed
        if timings is not unset:
            kwargs["timings"] = timings
        super().__init__(kwargs)
