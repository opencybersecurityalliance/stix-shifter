# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class GetTeamMembershipsSort(ModelSimple):
    """
    Specifies the order of returned team memberships

    :param value: Must be one of ["manager_name", "-manager_name", "name", "-name", "handle", "-handle", "email", "-email"].
    :type value: str
    """

    allowed_values = {
        "manager_name",
        "-manager_name",
        "name",
        "-name",
        "handle",
        "-handle",
        "email",
        "-email",
    }
    MANAGER_NAME: ClassVar["GetTeamMembershipsSort"]
    _MANAGER_NAME: ClassVar["GetTeamMembershipsSort"]
    NAME: ClassVar["GetTeamMembershipsSort"]
    _NAME: ClassVar["GetTeamMembershipsSort"]
    HANDLE: ClassVar["GetTeamMembershipsSort"]
    _HANDLE: ClassVar["GetTeamMembershipsSort"]
    EMAIL: ClassVar["GetTeamMembershipsSort"]
    _EMAIL: ClassVar["GetTeamMembershipsSort"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


GetTeamMembershipsSort.MANAGER_NAME = GetTeamMembershipsSort("manager_name")
GetTeamMembershipsSort._MANAGER_NAME = GetTeamMembershipsSort("-manager_name")
GetTeamMembershipsSort.NAME = GetTeamMembershipsSort("name")
GetTeamMembershipsSort._NAME = GetTeamMembershipsSort("-name")
GetTeamMembershipsSort.HANDLE = GetTeamMembershipsSort("handle")
GetTeamMembershipsSort._HANDLE = GetTeamMembershipsSort("-handle")
GetTeamMembershipsSort.EMAIL = GetTeamMembershipsSort("email")
GetTeamMembershipsSort._EMAIL = GetTeamMembershipsSort("-email")
