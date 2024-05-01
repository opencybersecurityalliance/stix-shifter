# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class RolesSort(ModelSimple):
    """
    Sorting options for roles.

    :param value: If omitted defaults to "name". Must be one of ["name", "-name", "modified_at", "-modified_at", "user_count", "-user_count"].
    :type value: str
    """

    allowed_values = {
        "name",
        "-name",
        "modified_at",
        "-modified_at",
        "user_count",
        "-user_count",
    }
    NAME_ASCENDING: ClassVar["RolesSort"]
    NAME_DESCENDING: ClassVar["RolesSort"]
    MODIFIED_AT_ASCENDING: ClassVar["RolesSort"]
    MODIFIED_AT_DESCENDING: ClassVar["RolesSort"]
    USER_COUNT_ASCENDING: ClassVar["RolesSort"]
    USER_COUNT_DESCENDING: ClassVar["RolesSort"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


RolesSort.NAME_ASCENDING = RolesSort("name")
RolesSort.NAME_DESCENDING = RolesSort("-name")
RolesSort.MODIFIED_AT_ASCENDING = RolesSort("modified_at")
RolesSort.MODIFIED_AT_DESCENDING = RolesSort("-modified_at")
RolesSort.USER_COUNT_ASCENDING = RolesSort("user_count")
RolesSort.USER_COUNT_DESCENDING = RolesSort("-user_count")
