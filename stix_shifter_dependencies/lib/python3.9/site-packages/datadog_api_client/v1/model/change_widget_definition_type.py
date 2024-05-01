# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class ChangeWidgetDefinitionType(ModelSimple):
    """
    Type of the change widget.

    :param value: If omitted defaults to "change". Must be one of ["change"].
    :type value: str
    """

    allowed_values = {
        "change",
    }
    CHANGE: ClassVar["ChangeWidgetDefinitionType"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


ChangeWidgetDefinitionType.CHANGE = ChangeWidgetDefinitionType("change")
