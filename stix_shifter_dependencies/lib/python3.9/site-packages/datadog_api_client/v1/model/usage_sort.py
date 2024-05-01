# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class UsageSort(ModelSimple):
    """
    The field to sort by.

    :param value: If omitted defaults to "start_date". Must be one of ["computed_on", "size", "start_date", "end_date"].
    :type value: str
    """

    allowed_values = {
        "computed_on",
        "size",
        "start_date",
        "end_date",
    }
    COMPUTED_ON: ClassVar["UsageSort"]
    SIZE: ClassVar["UsageSort"]
    START_DATE: ClassVar["UsageSort"]
    END_DATE: ClassVar["UsageSort"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


UsageSort.COMPUTED_ON = UsageSort("computed_on")
UsageSort.SIZE = UsageSort("size")
UsageSort.START_DATE = UsageSort("start_date")
UsageSort.END_DATE = UsageSort("end_date")
