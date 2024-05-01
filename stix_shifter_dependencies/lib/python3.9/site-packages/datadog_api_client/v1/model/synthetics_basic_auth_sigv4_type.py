# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class SyntheticsBasicAuthSigv4Type(ModelSimple):
    """
    The type of authentication to use when performing the test.

    :param value: If omitted defaults to "sigv4". Must be one of ["sigv4"].
    :type value: str
    """

    allowed_values = {
        "sigv4",
    }
    SIGV4: ClassVar["SyntheticsBasicAuthSigv4Type"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


SyntheticsBasicAuthSigv4Type.SIGV4 = SyntheticsBasicAuthSigv4Type("sigv4")
