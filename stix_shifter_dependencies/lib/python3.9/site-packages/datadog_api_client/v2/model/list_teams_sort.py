# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class ListTeamsSort(ModelSimple):
    """
    Specifies the order of the returned teams

    :param value: Must be one of ["name", "-name", "user_count", "-user_count"].
    :type value: str
    """

    allowed_values = {
        "name",
        "-name",
        "user_count",
        "-user_count",
    }
    NAME: ClassVar["ListTeamsSort"]
    _NAME: ClassVar["ListTeamsSort"]
    USER_COUNT: ClassVar["ListTeamsSort"]
    _USER_COUNT: ClassVar["ListTeamsSort"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


ListTeamsSort.NAME = ListTeamsSort("name")
ListTeamsSort._NAME = ListTeamsSort("-name")
ListTeamsSort.USER_COUNT = ListTeamsSort("user_count")
ListTeamsSort._USER_COUNT = ListTeamsSort("-user_count")
