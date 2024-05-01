# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class SecurityMonitoringFilterAction(ModelSimple):
    """
    The type of filtering action.

    :param value: Must be one of ["require", "suppress"].
    :type value: str
    """

    allowed_values = {
        "require",
        "suppress",
    }
    REQUIRE: ClassVar["SecurityMonitoringFilterAction"]
    SUPPRESS: ClassVar["SecurityMonitoringFilterAction"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


SecurityMonitoringFilterAction.REQUIRE = SecurityMonitoringFilterAction("require")
SecurityMonitoringFilterAction.SUPPRESS = SecurityMonitoringFilterAction("suppress")
