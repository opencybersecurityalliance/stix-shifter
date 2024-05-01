# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class ApplicationKeysSort(ModelSimple):
    """
    Sorting options

    :param value: If omitted defaults to "name". Must be one of ["created_at", "-created_at", "last4", "-last4", "name", "-name"].
    :type value: str
    """

    allowed_values = {
        "created_at",
        "-created_at",
        "last4",
        "-last4",
        "name",
        "-name",
    }
    CREATED_AT_ASCENDING: ClassVar["ApplicationKeysSort"]
    CREATED_AT_DESCENDING: ClassVar["ApplicationKeysSort"]
    LAST4_ASCENDING: ClassVar["ApplicationKeysSort"]
    LAST4_DESCENDING: ClassVar["ApplicationKeysSort"]
    NAME_ASCENDING: ClassVar["ApplicationKeysSort"]
    NAME_DESCENDING: ClassVar["ApplicationKeysSort"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


ApplicationKeysSort.CREATED_AT_ASCENDING = ApplicationKeysSort("created_at")
ApplicationKeysSort.CREATED_AT_DESCENDING = ApplicationKeysSort("-created_at")
ApplicationKeysSort.LAST4_ASCENDING = ApplicationKeysSort("last4")
ApplicationKeysSort.LAST4_DESCENDING = ApplicationKeysSort("-last4")
ApplicationKeysSort.NAME_ASCENDING = ApplicationKeysSort("name")
ApplicationKeysSort.NAME_DESCENDING = ApplicationKeysSort("-name")
