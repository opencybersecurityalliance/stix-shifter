# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class DashboardShareType(ModelSimple):
    """
    Type of sharing access (either open to anyone who has the public URL or invite-only).

    :param value: Must be one of ["open", "invite"].
    :type value: str
    """

    allowed_values = {
        "open",
        "invite",
    }
    OPEN: ClassVar["DashboardShareType"]
    INVITE: ClassVar["DashboardShareType"]

    _nullable = True

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


DashboardShareType.OPEN = DashboardShareType("open")
DashboardShareType.INVITE = DashboardShareType("invite")
