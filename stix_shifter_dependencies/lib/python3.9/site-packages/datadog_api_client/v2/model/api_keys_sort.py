# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class APIKeysSort(ModelSimple):
    """
    Sorting options

    :param value: If omitted defaults to "name". Must be one of ["created_at", "-created_at", "last4", "-last4", "modified_at", "-modified_at", "name", "-name"].
    :type value: str
    """

    allowed_values = {
        "created_at",
        "-created_at",
        "last4",
        "-last4",
        "modified_at",
        "-modified_at",
        "name",
        "-name",
    }
    CREATED_AT_ASCENDING: ClassVar["APIKeysSort"]
    CREATED_AT_DESCENDING: ClassVar["APIKeysSort"]
    LAST4_ASCENDING: ClassVar["APIKeysSort"]
    LAST4_DESCENDING: ClassVar["APIKeysSort"]
    MODIFIED_AT_ASCENDING: ClassVar["APIKeysSort"]
    MODIFIED_AT_DESCENDING: ClassVar["APIKeysSort"]
    NAME_ASCENDING: ClassVar["APIKeysSort"]
    NAME_DESCENDING: ClassVar["APIKeysSort"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


APIKeysSort.CREATED_AT_ASCENDING = APIKeysSort("created_at")
APIKeysSort.CREATED_AT_DESCENDING = APIKeysSort("-created_at")
APIKeysSort.LAST4_ASCENDING = APIKeysSort("last4")
APIKeysSort.LAST4_DESCENDING = APIKeysSort("-last4")
APIKeysSort.MODIFIED_AT_ASCENDING = APIKeysSort("modified_at")
APIKeysSort.MODIFIED_AT_DESCENDING = APIKeysSort("-modified_at")
APIKeysSort.NAME_ASCENDING = APIKeysSort("name")
APIKeysSort.NAME_DESCENDING = APIKeysSort("-name")
