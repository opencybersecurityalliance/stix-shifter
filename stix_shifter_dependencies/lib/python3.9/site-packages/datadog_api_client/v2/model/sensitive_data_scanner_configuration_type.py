# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class SensitiveDataScannerConfigurationType(ModelSimple):
    """
    Sensitive Data Scanner configuration type.

    :param value: If omitted defaults to "sensitive_data_scanner_configuration". Must be one of ["sensitive_data_scanner_configuration"].
    :type value: str
    """

    allowed_values = {
        "sensitive_data_scanner_configuration",
    }
    SENSITIVE_DATA_SCANNER_CONFIGURATIONS: ClassVar["SensitiveDataScannerConfigurationType"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


SensitiveDataScannerConfigurationType.SENSITIVE_DATA_SCANNER_CONFIGURATIONS = SensitiveDataScannerConfigurationType(
    "sensitive_data_scanner_configuration"
)
