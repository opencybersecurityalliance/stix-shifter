# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class LogsArchiveOrderDefinitionType(ModelSimple):
    """
    Type of the archive order definition.

    :param value: If omitted defaults to "archive_order". Must be one of ["archive_order"].
    :type value: str
    """

    allowed_values = {
        "archive_order",
    }
    ARCHIVE_ORDER: ClassVar["LogsArchiveOrderDefinitionType"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


LogsArchiveOrderDefinitionType.ARCHIVE_ORDER = LogsArchiveOrderDefinitionType("archive_order")
