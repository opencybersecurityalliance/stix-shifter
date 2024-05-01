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
    from datadog_api_client.v1.model.synthetics_trigger_ci_test_location import SyntheticsTriggerCITestLocation
    from datadog_api_client.v1.model.synthetics_trigger_ci_test_run_result import SyntheticsTriggerCITestRunResult


class SyntheticsTriggerCITestsResponse(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.synthetics_trigger_ci_test_location import SyntheticsTriggerCITestLocation
        from datadog_api_client.v1.model.synthetics_trigger_ci_test_run_result import SyntheticsTriggerCITestRunResult

        return {
            "batch_id": (str, none_type),
            "locations": ([SyntheticsTriggerCITestLocation],),
            "results": ([SyntheticsTriggerCITestRunResult],),
            "triggered_check_ids": ([str],),
        }

    attribute_map = {
        "batch_id": "batch_id",
        "locations": "locations",
        "results": "results",
        "triggered_check_ids": "triggered_check_ids",
    }

    def __init__(
        self_,
        batch_id: Union[str, none_type, UnsetType] = unset,
        locations: Union[List[SyntheticsTriggerCITestLocation], UnsetType] = unset,
        results: Union[List[SyntheticsTriggerCITestRunResult], UnsetType] = unset,
        triggered_check_ids: Union[List[str], UnsetType] = unset,
        **kwargs,
    ):
        """
        Object containing information about the tests triggered.

        :param batch_id: The public ID of the batch triggered.
        :type batch_id: str, none_type, optional

        :param locations: List of Synthetics locations.
        :type locations: [SyntheticsTriggerCITestLocation], optional

        :param results: Information about the tests runs.
        :type results: [SyntheticsTriggerCITestRunResult], optional

        :param triggered_check_ids: The public IDs of the Synthetics test triggered.
        :type triggered_check_ids: [str], optional
        """
        if batch_id is not unset:
            kwargs["batch_id"] = batch_id
        if locations is not unset:
            kwargs["locations"] = locations
        if results is not unset:
            kwargs["results"] = results
        if triggered_check_ids is not unset:
            kwargs["triggered_check_ids"] = triggered_check_ids
        super().__init__(kwargs)
