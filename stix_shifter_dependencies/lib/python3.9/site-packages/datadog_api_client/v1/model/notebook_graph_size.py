# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class NotebookGraphSize(ModelSimple):
    """
    The size of the graph.

    :param value: Must be one of ["xs", "s", "m", "l", "xl"].
    :type value: str
    """

    allowed_values = {
        "xs",
        "s",
        "m",
        "l",
        "xl",
    }
    EXTRA_SMALL: ClassVar["NotebookGraphSize"]
    SMALL: ClassVar["NotebookGraphSize"]
    MEDIUM: ClassVar["NotebookGraphSize"]
    LARGE: ClassVar["NotebookGraphSize"]
    EXTRA_LARGE: ClassVar["NotebookGraphSize"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


NotebookGraphSize.EXTRA_SMALL = NotebookGraphSize("xs")
NotebookGraphSize.SMALL = NotebookGraphSize("s")
NotebookGraphSize.MEDIUM = NotebookGraphSize("m")
NotebookGraphSize.LARGE = NotebookGraphSize("l")
NotebookGraphSize.EXTRA_LARGE = NotebookGraphSize("xl")
