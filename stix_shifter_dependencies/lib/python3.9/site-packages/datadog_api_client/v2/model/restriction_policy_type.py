# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class RestrictionPolicyType(ModelSimple):
    """
    Restriction policy type.

    :param value: If omitted defaults to "restriction_policy". Must be one of ["restriction_policy"].
    :type value: str
    """

    allowed_values = {
        "restriction_policy",
    }
    RESTRICTION_POLICY: ClassVar["RestrictionPolicyType"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


RestrictionPolicyType.RESTRICTION_POLICY = RestrictionPolicyType("restriction_policy")
