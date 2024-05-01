# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class NotebookCellResourceType(ModelSimple):
    """
    Type of the Notebook Cell resource.

    :param value: If omitted defaults to "notebook_cells". Must be one of ["notebook_cells"].
    :type value: str
    """

    allowed_values = {
        "notebook_cells",
    }
    NOTEBOOK_CELLS: ClassVar["NotebookCellResourceType"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


NotebookCellResourceType.NOTEBOOK_CELLS = NotebookCellResourceType("notebook_cells")
