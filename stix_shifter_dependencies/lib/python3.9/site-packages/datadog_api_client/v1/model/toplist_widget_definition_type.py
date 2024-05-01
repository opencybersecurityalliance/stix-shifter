# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class ToplistWidgetDefinitionType(ModelSimple):
    """
    Type of the top list widget.

    :param value: If omitted defaults to "toplist". Must be one of ["toplist"].
    :type value: str
    """

    allowed_values = {
        "toplist",
    }
    TOPLIST: ClassVar["ToplistWidgetDefinitionType"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


ToplistWidgetDefinitionType.TOPLIST = ToplistWidgetDefinitionType("toplist")
