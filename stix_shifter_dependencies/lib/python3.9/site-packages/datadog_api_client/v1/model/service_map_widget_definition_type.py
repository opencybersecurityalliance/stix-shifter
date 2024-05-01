# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class ServiceMapWidgetDefinitionType(ModelSimple):
    """
    Type of the service map widget.

    :param value: If omitted defaults to "servicemap". Must be one of ["servicemap"].
    :type value: str
    """

    allowed_values = {
        "servicemap",
    }
    SERVICEMAP: ClassVar["ServiceMapWidgetDefinitionType"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


ServiceMapWidgetDefinitionType.SERVICEMAP = ServiceMapWidgetDefinitionType("servicemap")
