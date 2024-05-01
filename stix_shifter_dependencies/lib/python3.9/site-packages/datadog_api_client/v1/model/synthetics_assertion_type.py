# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class SyntheticsAssertionType(ModelSimple):
    """
    Type of the assertion.

    :param value: Must be one of ["body", "header", "statusCode", "certificate", "responseTime", "property", "recordEvery", "recordSome", "tlsVersion", "minTlsVersion", "latency", "packetLossPercentage", "packetsReceived", "networkHop", "receivedMessage", "grpcHealthcheckStatus", "connection"].
    :type value: str
    """

    allowed_values = {
        "body",
        "header",
        "statusCode",
        "certificate",
        "responseTime",
        "property",
        "recordEvery",
        "recordSome",
        "tlsVersion",
        "minTlsVersion",
        "latency",
        "packetLossPercentage",
        "packetsReceived",
        "networkHop",
        "receivedMessage",
        "grpcHealthcheckStatus",
        "connection",
    }
    BODY: ClassVar["SyntheticsAssertionType"]
    HEADER: ClassVar["SyntheticsAssertionType"]
    STATUS_CODE: ClassVar["SyntheticsAssertionType"]
    CERTIFICATE: ClassVar["SyntheticsAssertionType"]
    RESPONSE_TIME: ClassVar["SyntheticsAssertionType"]
    PROPERTY: ClassVar["SyntheticsAssertionType"]
    RECORD_EVERY: ClassVar["SyntheticsAssertionType"]
    RECORD_SOME: ClassVar["SyntheticsAssertionType"]
    TLS_VERSION: ClassVar["SyntheticsAssertionType"]
    MIN_TLS_VERSION: ClassVar["SyntheticsAssertionType"]
    LATENCY: ClassVar["SyntheticsAssertionType"]
    PACKET_LOSS_PERCENTAGE: ClassVar["SyntheticsAssertionType"]
    PACKETS_RECEIVED: ClassVar["SyntheticsAssertionType"]
    NETWORK_HOP: ClassVar["SyntheticsAssertionType"]
    RECEIVED_MESSAGE: ClassVar["SyntheticsAssertionType"]
    GRPC_HEALTHCHECK_STATUS: ClassVar["SyntheticsAssertionType"]
    CONNECTION: ClassVar["SyntheticsAssertionType"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


SyntheticsAssertionType.BODY = SyntheticsAssertionType("body")
SyntheticsAssertionType.HEADER = SyntheticsAssertionType("header")
SyntheticsAssertionType.STATUS_CODE = SyntheticsAssertionType("statusCode")
SyntheticsAssertionType.CERTIFICATE = SyntheticsAssertionType("certificate")
SyntheticsAssertionType.RESPONSE_TIME = SyntheticsAssertionType("responseTime")
SyntheticsAssertionType.PROPERTY = SyntheticsAssertionType("property")
SyntheticsAssertionType.RECORD_EVERY = SyntheticsAssertionType("recordEvery")
SyntheticsAssertionType.RECORD_SOME = SyntheticsAssertionType("recordSome")
SyntheticsAssertionType.TLS_VERSION = SyntheticsAssertionType("tlsVersion")
SyntheticsAssertionType.MIN_TLS_VERSION = SyntheticsAssertionType("minTlsVersion")
SyntheticsAssertionType.LATENCY = SyntheticsAssertionType("latency")
SyntheticsAssertionType.PACKET_LOSS_PERCENTAGE = SyntheticsAssertionType("packetLossPercentage")
SyntheticsAssertionType.PACKETS_RECEIVED = SyntheticsAssertionType("packetsReceived")
SyntheticsAssertionType.NETWORK_HOP = SyntheticsAssertionType("networkHop")
SyntheticsAssertionType.RECEIVED_MESSAGE = SyntheticsAssertionType("receivedMessage")
SyntheticsAssertionType.GRPC_HEALTHCHECK_STATUS = SyntheticsAssertionType("grpcHealthcheckStatus")
SyntheticsAssertionType.CONNECTION = SyntheticsAssertionType("connection")
