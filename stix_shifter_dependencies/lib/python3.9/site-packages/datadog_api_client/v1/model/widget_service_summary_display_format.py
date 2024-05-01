# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class WidgetServiceSummaryDisplayFormat(ModelSimple):
    """
    Number of columns to display.

    :param value: Must be one of ["one_column", "two_column", "three_column"].
    :type value: str
    """

    allowed_values = {
        "one_column",
        "two_column",
        "three_column",
    }
    ONE_COLUMN: ClassVar["WidgetServiceSummaryDisplayFormat"]
    TWO_COLUMN: ClassVar["WidgetServiceSummaryDisplayFormat"]
    THREE_COLUMN: ClassVar["WidgetServiceSummaryDisplayFormat"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


WidgetServiceSummaryDisplayFormat.ONE_COLUMN = WidgetServiceSummaryDisplayFormat("one_column")
WidgetServiceSummaryDisplayFormat.TWO_COLUMN = WidgetServiceSummaryDisplayFormat("two_column")
WidgetServiceSummaryDisplayFormat.THREE_COLUMN = WidgetServiceSummaryDisplayFormat("three_column")
