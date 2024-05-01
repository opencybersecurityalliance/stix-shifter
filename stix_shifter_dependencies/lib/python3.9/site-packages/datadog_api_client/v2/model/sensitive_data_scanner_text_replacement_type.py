# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class SensitiveDataScannerTextReplacementType(ModelSimple):
    """
    Type of the replacement text. None means no replacement.
        hash means the data will be stubbed. replacement_string means that
        one can chose a text to replace the data. partial_replacement_from_beginning
        allows a user to partially replace the data from the beginning, and
        partial_replacement_from_end on the other hand, allows to replace data from
        the end.

    :param value: If omitted defaults to "none". Must be one of ["none", "hash", "replacement_string", "partial_replacement_from_beginning", "partial_replacement_from_end"].
    :type value: str
    """

    allowed_values = {
        "none",
        "hash",
        "replacement_string",
        "partial_replacement_from_beginning",
        "partial_replacement_from_end",
    }
    NONE: ClassVar["SensitiveDataScannerTextReplacementType"]
    HASH: ClassVar["SensitiveDataScannerTextReplacementType"]
    REPLACEMENT_STRING: ClassVar["SensitiveDataScannerTextReplacementType"]
    PARTIAL_REPLACEMENT_FROM_BEGINNING: ClassVar["SensitiveDataScannerTextReplacementType"]
    PARTIAL_REPLACEMENT_FROM_END: ClassVar["SensitiveDataScannerTextReplacementType"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


SensitiveDataScannerTextReplacementType.NONE = SensitiveDataScannerTextReplacementType("none")
SensitiveDataScannerTextReplacementType.HASH = SensitiveDataScannerTextReplacementType("hash")
SensitiveDataScannerTextReplacementType.REPLACEMENT_STRING = SensitiveDataScannerTextReplacementType(
    "replacement_string"
)
SensitiveDataScannerTextReplacementType.PARTIAL_REPLACEMENT_FROM_BEGINNING = SensitiveDataScannerTextReplacementType(
    "partial_replacement_from_beginning"
)
SensitiveDataScannerTextReplacementType.PARTIAL_REPLACEMENT_FROM_END = SensitiveDataScannerTextReplacementType(
    "partial_replacement_from_end"
)
