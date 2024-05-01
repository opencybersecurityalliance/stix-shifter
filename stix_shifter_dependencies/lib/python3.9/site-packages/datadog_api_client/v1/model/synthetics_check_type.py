# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class SyntheticsCheckType(ModelSimple):
    """
    Type of assertion to apply in an API test.

    :param value: Must be one of ["equals", "notEquals", "contains", "notContains", "startsWith", "notStartsWith", "greater", "lower", "greaterEquals", "lowerEquals", "matchRegex", "between", "isEmpty", "notIsEmpty"].
    :type value: str
    """

    allowed_values = {
        "equals",
        "notEquals",
        "contains",
        "notContains",
        "startsWith",
        "notStartsWith",
        "greater",
        "lower",
        "greaterEquals",
        "lowerEquals",
        "matchRegex",
        "between",
        "isEmpty",
        "notIsEmpty",
    }
    EQUALS: ClassVar["SyntheticsCheckType"]
    NOT_EQUALS: ClassVar["SyntheticsCheckType"]
    CONTAINS: ClassVar["SyntheticsCheckType"]
    NOT_CONTAINS: ClassVar["SyntheticsCheckType"]
    STARTS_WITH: ClassVar["SyntheticsCheckType"]
    NOT_STARTS_WITH: ClassVar["SyntheticsCheckType"]
    GREATER: ClassVar["SyntheticsCheckType"]
    LOWER: ClassVar["SyntheticsCheckType"]
    GREATER_EQUALS: ClassVar["SyntheticsCheckType"]
    LOWER_EQUALS: ClassVar["SyntheticsCheckType"]
    MATCH_REGEX: ClassVar["SyntheticsCheckType"]
    BETWEEN: ClassVar["SyntheticsCheckType"]
    IS_EMPTY: ClassVar["SyntheticsCheckType"]
    NOT_IS_EMPTY: ClassVar["SyntheticsCheckType"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


SyntheticsCheckType.EQUALS = SyntheticsCheckType("equals")
SyntheticsCheckType.NOT_EQUALS = SyntheticsCheckType("notEquals")
SyntheticsCheckType.CONTAINS = SyntheticsCheckType("contains")
SyntheticsCheckType.NOT_CONTAINS = SyntheticsCheckType("notContains")
SyntheticsCheckType.STARTS_WITH = SyntheticsCheckType("startsWith")
SyntheticsCheckType.NOT_STARTS_WITH = SyntheticsCheckType("notStartsWith")
SyntheticsCheckType.GREATER = SyntheticsCheckType("greater")
SyntheticsCheckType.LOWER = SyntheticsCheckType("lower")
SyntheticsCheckType.GREATER_EQUALS = SyntheticsCheckType("greaterEquals")
SyntheticsCheckType.LOWER_EQUALS = SyntheticsCheckType("lowerEquals")
SyntheticsCheckType.MATCH_REGEX = SyntheticsCheckType("matchRegex")
SyntheticsCheckType.BETWEEN = SyntheticsCheckType("between")
SyntheticsCheckType.IS_EMPTY = SyntheticsCheckType("isEmpty")
SyntheticsCheckType.NOT_IS_EMPTY = SyntheticsCheckType("notIsEmpty")
