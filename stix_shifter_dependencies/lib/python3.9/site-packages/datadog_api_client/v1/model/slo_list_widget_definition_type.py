# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class SLOListWidgetDefinitionType(ModelSimple):
    """
    Type of the SLO List widget.

    :param value: If omitted defaults to "slo_list". Must be one of ["slo_list"].
    :type value: str
    """

    allowed_values = {
        "slo_list",
    }
    SLO_LIST: ClassVar["SLOListWidgetDefinitionType"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


SLOListWidgetDefinitionType.SLO_LIST = SLOListWidgetDefinitionType("slo_list")
