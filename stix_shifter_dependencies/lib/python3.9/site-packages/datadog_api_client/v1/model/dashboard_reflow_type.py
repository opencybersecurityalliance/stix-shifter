# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class DashboardReflowType(ModelSimple):
    """
    Reflow type for a **new dashboard layout** dashboard. Set this only when layout type is 'ordered'.
        If set to 'fixed', the dashboard expects all widgets to have a layout, and if it's set to 'auto',
        widgets should not have layouts.

    :param value: Must be one of ["auto", "fixed"].
    :type value: str
    """

    allowed_values = {
        "auto",
        "fixed",
    }
    AUTO: ClassVar["DashboardReflowType"]
    FIXED: ClassVar["DashboardReflowType"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


DashboardReflowType.AUTO = DashboardReflowType("auto")
DashboardReflowType.FIXED = DashboardReflowType("fixed")
