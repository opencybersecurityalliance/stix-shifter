# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class MonitorOptionsNotificationPresets(ModelSimple):
    """
    Toggles the display of additional content sent in the monitor notification.

    :param value: If omitted defaults to "show_all". Must be one of ["show_all", "hide_query", "hide_handles", "hide_all"].
    :type value: str
    """

    allowed_values = {
        "show_all",
        "hide_query",
        "hide_handles",
        "hide_all",
    }
    SHOW_ALL: ClassVar["MonitorOptionsNotificationPresets"]
    HIDE_QUERY: ClassVar["MonitorOptionsNotificationPresets"]
    HIDE_HANDLES: ClassVar["MonitorOptionsNotificationPresets"]
    HIDE_ALL: ClassVar["MonitorOptionsNotificationPresets"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


MonitorOptionsNotificationPresets.SHOW_ALL = MonitorOptionsNotificationPresets("show_all")
MonitorOptionsNotificationPresets.HIDE_QUERY = MonitorOptionsNotificationPresets("hide_query")
MonitorOptionsNotificationPresets.HIDE_HANDLES = MonitorOptionsNotificationPresets("hide_handles")
MonitorOptionsNotificationPresets.HIDE_ALL = MonitorOptionsNotificationPresets("hide_all")
