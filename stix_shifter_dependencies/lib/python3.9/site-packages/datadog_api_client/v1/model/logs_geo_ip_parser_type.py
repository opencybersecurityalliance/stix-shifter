# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class LogsGeoIPParserType(ModelSimple):
    """
    Type of GeoIP parser.

    :param value: If omitted defaults to "geo-ip-parser". Must be one of ["geo-ip-parser"].
    :type value: str
    """

    allowed_values = {
        "geo-ip-parser",
    }
    GEO_IP_PARSER: ClassVar["LogsGeoIPParserType"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


LogsGeoIPParserType.GEO_IP_PARSER = LogsGeoIPParserType("geo-ip-parser")
