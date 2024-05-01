# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class WidgetViewMode(ModelSimple):
    """
    Define how you want the SLO to be displayed.

    :param value: Must be one of ["overall", "component", "both"].
    :type value: str
    """

    allowed_values = {
        "overall",
        "component",
        "both",
    }
    OVERALL: ClassVar["WidgetViewMode"]
    COMPONENT: ClassVar["WidgetViewMode"]
    BOTH: ClassVar["WidgetViewMode"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


WidgetViewMode.OVERALL = WidgetViewMode("overall")
WidgetViewMode.COMPONENT = WidgetViewMode("component")
WidgetViewMode.BOTH = WidgetViewMode("both")
