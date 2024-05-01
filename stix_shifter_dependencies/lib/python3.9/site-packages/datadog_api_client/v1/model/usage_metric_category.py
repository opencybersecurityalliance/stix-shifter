# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class UsageMetricCategory(ModelSimple):
    """
    Contains the metric category.

    :param value: Must be one of ["standard", "custom"].
    :type value: str
    """

    allowed_values = {
        "standard",
        "custom",
    }
    STANDARD: ClassVar["UsageMetricCategory"]
    CUSTOM: ClassVar["UsageMetricCategory"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


UsageMetricCategory.STANDARD = UsageMetricCategory("standard")
UsageMetricCategory.CUSTOM = UsageMetricCategory("custom")
