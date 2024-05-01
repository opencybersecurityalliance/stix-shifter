# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class SyntheticsTestDetailsSubType(ModelSimple):
    """
    The subtype of the Synthetic API test, `http`, `ssl`, `tcp`,
        `dns`, `icmp`, `udp`, `websocket`, `grpc` or `multi`.

    :param value: Must be one of ["http", "ssl", "tcp", "dns", "multi", "icmp", "udp", "websocket", "grpc"].
    :type value: str
    """

    allowed_values = {
        "http",
        "ssl",
        "tcp",
        "dns",
        "multi",
        "icmp",
        "udp",
        "websocket",
        "grpc",
    }
    HTTP: ClassVar["SyntheticsTestDetailsSubType"]
    SSL: ClassVar["SyntheticsTestDetailsSubType"]
    TCP: ClassVar["SyntheticsTestDetailsSubType"]
    DNS: ClassVar["SyntheticsTestDetailsSubType"]
    MULTI: ClassVar["SyntheticsTestDetailsSubType"]
    ICMP: ClassVar["SyntheticsTestDetailsSubType"]
    UDP: ClassVar["SyntheticsTestDetailsSubType"]
    WEBSOCKET: ClassVar["SyntheticsTestDetailsSubType"]
    GRPC: ClassVar["SyntheticsTestDetailsSubType"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


SyntheticsTestDetailsSubType.HTTP = SyntheticsTestDetailsSubType("http")
SyntheticsTestDetailsSubType.SSL = SyntheticsTestDetailsSubType("ssl")
SyntheticsTestDetailsSubType.TCP = SyntheticsTestDetailsSubType("tcp")
SyntheticsTestDetailsSubType.DNS = SyntheticsTestDetailsSubType("dns")
SyntheticsTestDetailsSubType.MULTI = SyntheticsTestDetailsSubType("multi")
SyntheticsTestDetailsSubType.ICMP = SyntheticsTestDetailsSubType("icmp")
SyntheticsTestDetailsSubType.UDP = SyntheticsTestDetailsSubType("udp")
SyntheticsTestDetailsSubType.WEBSOCKET = SyntheticsTestDetailsSubType("websocket")
SyntheticsTestDetailsSubType.GRPC = SyntheticsTestDetailsSubType("grpc")
