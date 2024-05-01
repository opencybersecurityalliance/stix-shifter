# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class EventStatusType(ModelSimple):
    """
    If an alert event is enabled, its status is one of the following:
        `failure`, `error`, `warning`, `info`, `success`, `user_update`,
        `recommendation`, or `snapshot`.

    :param value: Must be one of ["failure", "error", "warning", "info", "success", "user_update", "recommendation", "snapshot"].
    :type value: str
    """

    allowed_values = {
        "failure",
        "error",
        "warning",
        "info",
        "success",
        "user_update",
        "recommendation",
        "snapshot",
    }
    FAILURE: ClassVar["EventStatusType"]
    ERROR: ClassVar["EventStatusType"]
    WARNING: ClassVar["EventStatusType"]
    INFO: ClassVar["EventStatusType"]
    SUCCESS: ClassVar["EventStatusType"]
    USER_UPDATE: ClassVar["EventStatusType"]
    RECOMMENDATION: ClassVar["EventStatusType"]
    SNAPSHOT: ClassVar["EventStatusType"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


EventStatusType.FAILURE = EventStatusType("failure")
EventStatusType.ERROR = EventStatusType("error")
EventStatusType.WARNING = EventStatusType("warning")
EventStatusType.INFO = EventStatusType("info")
EventStatusType.SUCCESS = EventStatusType("success")
EventStatusType.USER_UPDATE = EventStatusType("user_update")
EventStatusType.RECOMMENDATION = EventStatusType("recommendation")
EventStatusType.SNAPSHOT = EventStatusType("snapshot")
