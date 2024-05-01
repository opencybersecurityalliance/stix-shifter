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
    from datadog_api_client.v1.model.synthetics_test_details import SyntheticsTestDetails


class SyntheticsListTestsResponse(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.synthetics_test_details import SyntheticsTestDetails

        return {
            "tests": ([SyntheticsTestDetails],),
        }

    attribute_map = {
        "tests": "tests",
    }

    def __init__(self_, tests: Union[List[SyntheticsTestDetails], UnsetType] = unset, **kwargs):
        """
        Object containing an array of Synthetic tests configuration.

        :param tests: Array of Synthetic tests configuration.
        :type tests: [SyntheticsTestDetails], optional
        """
        if tests is not unset:
            kwargs["tests"] = tests
        super().__init__(kwargs)
