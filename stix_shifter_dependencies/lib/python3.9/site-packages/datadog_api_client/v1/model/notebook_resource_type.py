# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class NotebookResourceType(ModelSimple):
    """
    Type of the Notebook resource.

    :param value: If omitted defaults to "notebooks". Must be one of ["notebooks"].
    :type value: str
    """

    allowed_values = {
        "notebooks",
    }
    NOTEBOOKS: ClassVar["NotebookResourceType"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


NotebookResourceType.NOTEBOOKS = NotebookResourceType("notebooks")
