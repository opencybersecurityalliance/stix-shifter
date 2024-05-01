# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class SyntheticsAssertionOperator(ModelSimple):
    """
    Assertion operator to apply.

    :param value: Must be one of ["contains", "doesNotContain", "is", "isNot", "lessThan", "lessThanOrEqual", "moreThan", "moreThanOrEqual", "matches", "doesNotMatch", "validates", "isInMoreThan", "isInLessThan", "doesNotExist"].
    :type value: str
    """

    allowed_values = {
        "contains",
        "doesNotContain",
        "is",
        "isNot",
        "lessThan",
        "lessThanOrEqual",
        "moreThan",
        "moreThanOrEqual",
        "matches",
        "doesNotMatch",
        "validates",
        "isInMoreThan",
        "isInLessThan",
        "doesNotExist",
    }
    CONTAINS: ClassVar["SyntheticsAssertionOperator"]
    DOES_NOT_CONTAIN: ClassVar["SyntheticsAssertionOperator"]
    IS: ClassVar["SyntheticsAssertionOperator"]
    IS_NOT: ClassVar["SyntheticsAssertionOperator"]
    LESS_THAN: ClassVar["SyntheticsAssertionOperator"]
    LESS_THAN_OR_EQUAL: ClassVar["SyntheticsAssertionOperator"]
    MORE_THAN: ClassVar["SyntheticsAssertionOperator"]
    MORE_THAN_OR_EQUAL: ClassVar["SyntheticsAssertionOperator"]
    MATCHES: ClassVar["SyntheticsAssertionOperator"]
    DOES_NOT_MATCH: ClassVar["SyntheticsAssertionOperator"]
    VALIDATES: ClassVar["SyntheticsAssertionOperator"]
    IS_IN_MORE_DAYS_THAN: ClassVar["SyntheticsAssertionOperator"]
    IS_IN_LESS_DAYS_THAN: ClassVar["SyntheticsAssertionOperator"]
    DOES_NOT_EXIST: ClassVar["SyntheticsAssertionOperator"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


SyntheticsAssertionOperator.CONTAINS = SyntheticsAssertionOperator("contains")
SyntheticsAssertionOperator.DOES_NOT_CONTAIN = SyntheticsAssertionOperator("doesNotContain")
SyntheticsAssertionOperator.IS = SyntheticsAssertionOperator("is")
SyntheticsAssertionOperator.IS_NOT = SyntheticsAssertionOperator("isNot")
SyntheticsAssertionOperator.LESS_THAN = SyntheticsAssertionOperator("lessThan")
SyntheticsAssertionOperator.LESS_THAN_OR_EQUAL = SyntheticsAssertionOperator("lessThanOrEqual")
SyntheticsAssertionOperator.MORE_THAN = SyntheticsAssertionOperator("moreThan")
SyntheticsAssertionOperator.MORE_THAN_OR_EQUAL = SyntheticsAssertionOperator("moreThanOrEqual")
SyntheticsAssertionOperator.MATCHES = SyntheticsAssertionOperator("matches")
SyntheticsAssertionOperator.DOES_NOT_MATCH = SyntheticsAssertionOperator("doesNotMatch")
SyntheticsAssertionOperator.VALIDATES = SyntheticsAssertionOperator("validates")
SyntheticsAssertionOperator.IS_IN_MORE_DAYS_THAN = SyntheticsAssertionOperator("isInMoreThan")
SyntheticsAssertionOperator.IS_IN_LESS_DAYS_THAN = SyntheticsAssertionOperator("isInLessThan")
SyntheticsAssertionOperator.DOES_NOT_EXIST = SyntheticsAssertionOperator("doesNotExist")
