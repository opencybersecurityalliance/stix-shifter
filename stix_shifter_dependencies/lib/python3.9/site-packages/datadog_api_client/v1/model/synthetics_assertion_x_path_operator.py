# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class SyntheticsAssertionXPathOperator(ModelSimple):
    """
    Assertion operator to apply.

    :param value: If omitted defaults to "validatesXPath". Must be one of ["validatesXPath"].
    :type value: str
    """

    allowed_values = {
        "validatesXPath",
    }
    VALIDATES_X_PATH: ClassVar["SyntheticsAssertionXPathOperator"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


SyntheticsAssertionXPathOperator.VALIDATES_X_PATH = SyntheticsAssertionXPathOperator("validatesXPath")
