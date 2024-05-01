# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class SensitiveDataScannerGroupType(ModelSimple):
    """
    Sensitive Data Scanner group type.

    :param value: If omitted defaults to "sensitive_data_scanner_group". Must be one of ["sensitive_data_scanner_group"].
    :type value: str
    """

    allowed_values = {
        "sensitive_data_scanner_group",
    }
    SENSITIVE_DATA_SCANNER_GROUP: ClassVar["SensitiveDataScannerGroupType"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


SensitiveDataScannerGroupType.SENSITIVE_DATA_SCANNER_GROUP = SensitiveDataScannerGroupType(
    "sensitive_data_scanner_group"
)
