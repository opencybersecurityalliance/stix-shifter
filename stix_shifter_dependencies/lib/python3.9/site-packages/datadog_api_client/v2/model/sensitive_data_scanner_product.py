# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class SensitiveDataScannerProduct(ModelSimple):
    """
    Datadog product onto which Sensitive Data Scanner can be activated.

    :param value: If omitted defaults to "logs". Must be one of ["logs", "rum", "events", "apm"].
    :type value: str
    """

    allowed_values = {
        "logs",
        "rum",
        "events",
        "apm",
    }
    LOGS: ClassVar["SensitiveDataScannerProduct"]
    RUM: ClassVar["SensitiveDataScannerProduct"]
    EVENTS: ClassVar["SensitiveDataScannerProduct"]
    APM: ClassVar["SensitiveDataScannerProduct"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


SensitiveDataScannerProduct.LOGS = SensitiveDataScannerProduct("logs")
SensitiveDataScannerProduct.RUM = SensitiveDataScannerProduct("rum")
SensitiveDataScannerProduct.EVENTS = SensitiveDataScannerProduct("events")
SensitiveDataScannerProduct.APM = SensitiveDataScannerProduct("apm")
