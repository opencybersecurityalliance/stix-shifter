# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class WidgetOrderBy(ModelSimple):
    """
    What to order by.

    :param value: Must be one of ["change", "name", "present", "past"].
    :type value: str
    """

    allowed_values = {
        "change",
        "name",
        "present",
        "past",
    }
    CHANGE: ClassVar["WidgetOrderBy"]
    NAME: ClassVar["WidgetOrderBy"]
    PRESENT: ClassVar["WidgetOrderBy"]
    PAST: ClassVar["WidgetOrderBy"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


WidgetOrderBy.CHANGE = WidgetOrderBy("change")
WidgetOrderBy.NAME = WidgetOrderBy("name")
WidgetOrderBy.PRESENT = WidgetOrderBy("present")
WidgetOrderBy.PAST = WidgetOrderBy("past")
