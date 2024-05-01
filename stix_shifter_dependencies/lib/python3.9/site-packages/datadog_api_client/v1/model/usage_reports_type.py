# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class UsageReportsType(ModelSimple):
    """
    The type of reports.

    :param value: If omitted defaults to "reports". Must be one of ["reports"].
    :type value: str
    """

    allowed_values = {
        "reports",
    }
    REPORTS: ClassVar["UsageReportsType"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


UsageReportsType.REPORTS = UsageReportsType("reports")
