# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class WidgetMonitorSummarySort(ModelSimple):
    """
    Widget sorting methods.

    :param value: Must be one of ["name", "group", "status", "tags", "triggered", "group,asc", "group,desc", "name,asc", "name,desc", "status,asc", "status,desc", "tags,asc", "tags,desc", "triggered,asc", "triggered,desc", "priority,asc", "priority,desc"].
    :type value: str
    """

    allowed_values = {
        "name",
        "group",
        "status",
        "tags",
        "triggered",
        "group,asc",
        "group,desc",
        "name,asc",
        "name,desc",
        "status,asc",
        "status,desc",
        "tags,asc",
        "tags,desc",
        "triggered,asc",
        "triggered,desc",
        "priority,asc",
        "priority,desc",
    }
    NAME: ClassVar["WidgetMonitorSummarySort"]
    GROUP: ClassVar["WidgetMonitorSummarySort"]
    STATUS: ClassVar["WidgetMonitorSummarySort"]
    TAGS: ClassVar["WidgetMonitorSummarySort"]
    TRIGGERED: ClassVar["WidgetMonitorSummarySort"]
    GROUP_ASCENDING: ClassVar["WidgetMonitorSummarySort"]
    GROUP_DESCENDING: ClassVar["WidgetMonitorSummarySort"]
    NAME_ASCENDING: ClassVar["WidgetMonitorSummarySort"]
    NAME_DESCENDING: ClassVar["WidgetMonitorSummarySort"]
    STATUS_ASCENDING: ClassVar["WidgetMonitorSummarySort"]
    STATUS_DESCENDING: ClassVar["WidgetMonitorSummarySort"]
    TAGS_ASCENDING: ClassVar["WidgetMonitorSummarySort"]
    TAGS_DESCENDING: ClassVar["WidgetMonitorSummarySort"]
    TRIGGERED_ASCENDING: ClassVar["WidgetMonitorSummarySort"]
    TRIGGERED_DESCENDING: ClassVar["WidgetMonitorSummarySort"]
    PRIORITY_ASCENDING: ClassVar["WidgetMonitorSummarySort"]
    PRIORITY_DESCENDING: ClassVar["WidgetMonitorSummarySort"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


WidgetMonitorSummarySort.NAME = WidgetMonitorSummarySort("name")
WidgetMonitorSummarySort.GROUP = WidgetMonitorSummarySort("group")
WidgetMonitorSummarySort.STATUS = WidgetMonitorSummarySort("status")
WidgetMonitorSummarySort.TAGS = WidgetMonitorSummarySort("tags")
WidgetMonitorSummarySort.TRIGGERED = WidgetMonitorSummarySort("triggered")
WidgetMonitorSummarySort.GROUP_ASCENDING = WidgetMonitorSummarySort("group,asc")
WidgetMonitorSummarySort.GROUP_DESCENDING = WidgetMonitorSummarySort("group,desc")
WidgetMonitorSummarySort.NAME_ASCENDING = WidgetMonitorSummarySort("name,asc")
WidgetMonitorSummarySort.NAME_DESCENDING = WidgetMonitorSummarySort("name,desc")
WidgetMonitorSummarySort.STATUS_ASCENDING = WidgetMonitorSummarySort("status,asc")
WidgetMonitorSummarySort.STATUS_DESCENDING = WidgetMonitorSummarySort("status,desc")
WidgetMonitorSummarySort.TAGS_ASCENDING = WidgetMonitorSummarySort("tags,asc")
WidgetMonitorSummarySort.TAGS_DESCENDING = WidgetMonitorSummarySort("tags,desc")
WidgetMonitorSummarySort.TRIGGERED_ASCENDING = WidgetMonitorSummarySort("triggered,asc")
WidgetMonitorSummarySort.TRIGGERED_DESCENDING = WidgetMonitorSummarySort("triggered,desc")
WidgetMonitorSummarySort.PRIORITY_ASCENDING = WidgetMonitorSummarySort("priority,asc")
WidgetMonitorSummarySort.PRIORITY_DESCENDING = WidgetMonitorSummarySort("priority,desc")
