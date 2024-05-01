# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class ScalarFormulaRequestType(ModelSimple):
    """
    The type of the resource. The value should always be scalar_request.

    :param value: If omitted defaults to "scalar_request". Must be one of ["scalar_request"].
    :type value: str
    """

    allowed_values = {
        "scalar_request",
    }
    SCALAR_REQUEST: ClassVar["ScalarFormulaRequestType"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


ScalarFormulaRequestType.SCALAR_REQUEST = ScalarFormulaRequestType("scalar_request")
