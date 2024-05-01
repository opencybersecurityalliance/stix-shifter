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
    from datadog_api_client.v1.model.synthetics_ci_test import SyntheticsCITest


class SyntheticsCITestBody(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.synthetics_ci_test import SyntheticsCITest

        return {
            "tests": ([SyntheticsCITest],),
        }

    attribute_map = {
        "tests": "tests",
    }

    def __init__(self_, tests: Union[List[SyntheticsCITest], UnsetType] = unset, **kwargs):
        """
        Object describing the synthetics tests to trigger.

        :param tests: Individual synthetics test.
        :type tests: [SyntheticsCITest], optional
        """
        if tests is not unset:
            kwargs["tests"] = tests
        super().__init__(kwargs)
