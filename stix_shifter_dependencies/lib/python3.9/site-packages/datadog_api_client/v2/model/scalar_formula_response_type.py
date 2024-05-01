# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class ScalarFormulaResponseType(ModelSimple):
    """
    The type of the resource. The value should always be scalar_response.

    :param value: If omitted defaults to "scalar_response". Must be one of ["scalar_response"].
    :type value: str
    """

    allowed_values = {
        "scalar_response",
    }
    SCALAR_RESPONSE: ClassVar["ScalarFormulaResponseType"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


ScalarFormulaResponseType.SCALAR_RESPONSE = ScalarFormulaResponseType("scalar_response")
