# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Union, TYPE_CHECKING

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    unset,
    UnsetType,
)


if TYPE_CHECKING:
    from datadog_api_client.v2.model.sensitive_data_scanner_text_replacement_type import (
        SensitiveDataScannerTextReplacementType,
    )


class SensitiveDataScannerTextReplacement(ModelNormal):
    validations = {
        "number_of_chars": {
            "inclusive_minimum": 0,
        },
    }

    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.sensitive_data_scanner_text_replacement_type import (
            SensitiveDataScannerTextReplacementType,
        )

        return {
            "number_of_chars": (int,),
            "replacement_string": (str,),
            "type": (SensitiveDataScannerTextReplacementType,),
        }

    attribute_map = {
        "number_of_chars": "number_of_chars",
        "replacement_string": "replacement_string",
        "type": "type",
    }

    def __init__(
        self_,
        number_of_chars: Union[int, UnsetType] = unset,
        replacement_string: Union[str, UnsetType] = unset,
        type: Union[SensitiveDataScannerTextReplacementType, UnsetType] = unset,
        **kwargs,
    ):
        """
        Object describing how the scanned event will be replaced.

        :param number_of_chars: Required if type == 'partial_replacement_from_beginning'
            or 'partial_replacement_from_end'. It must be > 0.
        :type number_of_chars: int, optional

        :param replacement_string: Required if type == 'replacement_string'.
        :type replacement_string: str, optional

        :param type: Type of the replacement text. None means no replacement.
            hash means the data will be stubbed. replacement_string means that
            one can chose a text to replace the data. partial_replacement_from_beginning
            allows a user to partially replace the data from the beginning, and
            partial_replacement_from_end on the other hand, allows to replace data from
            the end.
        :type type: SensitiveDataScannerTextReplacementType, optional
        """
        if number_of_chars is not unset:
            kwargs["number_of_chars"] = number_of_chars
        if replacement_string is not unset:
            kwargs["replacement_string"] = replacement_string
        if type is not unset:
            kwargs["type"] = type
        super().__init__(kwargs)
