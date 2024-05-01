# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class EventsSortType(ModelSimple):
    """
    The type of sort to use on the calculated value.

    :param value: Must be one of ["alphabetical", "measure"].
    :type value: str
    """

    allowed_values = {
        "alphabetical",
        "measure",
    }
    ALPHABETICAL: ClassVar["EventsSortType"]
    MEASURE: ClassVar["EventsSortType"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


EventsSortType.ALPHABETICAL = EventsSortType("alphabetical")
EventsSortType.MEASURE = EventsSortType("measure")
