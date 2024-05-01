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
    from datadog_api_client.v1.model.synthetics_test_execution_rule import SyntheticsTestExecutionRule


class SyntheticsTestCiOptions(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.synthetics_test_execution_rule import SyntheticsTestExecutionRule

        return {
            "execution_rule": (SyntheticsTestExecutionRule,),
        }

    attribute_map = {
        "execution_rule": "executionRule",
    }

    def __init__(self_, execution_rule: Union[SyntheticsTestExecutionRule, UnsetType] = unset, **kwargs):
        """
        CI/CD options for a Synthetic test.

        :param execution_rule: Execution rule for a Synthetics test.
        :type execution_rule: SyntheticsTestExecutionRule, optional
        """
        if execution_rule is not unset:
            kwargs["execution_rule"] = execution_rule
        super().__init__(kwargs)
