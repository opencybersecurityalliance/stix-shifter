# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class SyntheticsTestExecutionRule(ModelSimple):
    """
    Execution rule for a Synthetics test.

    :param value: Must be one of ["blocking", "non_blocking", "skipped"].
    :type value: str
    """

    allowed_values = {
        "blocking",
        "non_blocking",
        "skipped",
    }
    BLOCKING: ClassVar["SyntheticsTestExecutionRule"]
    NON_BLOCKING: ClassVar["SyntheticsTestExecutionRule"]
    SKIPPED: ClassVar["SyntheticsTestExecutionRule"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


SyntheticsTestExecutionRule.BLOCKING = SyntheticsTestExecutionRule("blocking")
SyntheticsTestExecutionRule.NON_BLOCKING = SyntheticsTestExecutionRule("non_blocking")
SyntheticsTestExecutionRule.SKIPPED = SyntheticsTestExecutionRule("skipped")
