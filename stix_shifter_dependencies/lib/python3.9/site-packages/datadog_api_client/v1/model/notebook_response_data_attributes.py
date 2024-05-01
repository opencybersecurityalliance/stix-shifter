# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import List, Union, TYPE_CHECKING

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    datetime,
    unset,
    UnsetType,
)


if TYPE_CHECKING:
    from datadog_api_client.v1.model.notebook_author import NotebookAuthor
    from datadog_api_client.v1.model.notebook_cell_response import NotebookCellResponse
    from datadog_api_client.v1.model.notebook_metadata import NotebookMetadata
    from datadog_api_client.v1.model.notebook_status import NotebookStatus
    from datadog_api_client.v1.model.notebook_global_time import NotebookGlobalTime
    from datadog_api_client.v1.model.notebook_relative_time import NotebookRelativeTime
    from datadog_api_client.v1.model.notebook_absolute_time import NotebookAbsoluteTime


class NotebookResponseDataAttributes(ModelNormal):
    validations = {
        "name": {
            "max_length": 80,
            "min_length": 0,
        },
    }

    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.notebook_author import NotebookAuthor
        from datadog_api_client.v1.model.notebook_cell_response import NotebookCellResponse
        from datadog_api_client.v1.model.notebook_metadata import NotebookMetadata
        from datadog_api_client.v1.model.notebook_status import NotebookStatus
        from datadog_api_client.v1.model.notebook_global_time import NotebookGlobalTime

        return {
            "author": (NotebookAuthor,),
            "cells": ([NotebookCellResponse],),
            "created": (datetime,),
            "metadata": (NotebookMetadata,),
            "modified": (datetime,),
            "name": (str,),
            "status": (NotebookStatus,),
            "time": (NotebookGlobalTime,),
        }

    attribute_map = {
        "author": "author",
        "cells": "cells",
        "created": "created",
        "metadata": "metadata",
        "modified": "modified",
        "name": "name",
        "status": "status",
        "time": "time",
    }
    read_only_vars = {
        "created",
        "modified",
    }

    def __init__(
        self_,
        cells: List[NotebookCellResponse],
        name: str,
        time: Union[NotebookGlobalTime, NotebookRelativeTime, NotebookAbsoluteTime],
        author: Union[NotebookAuthor, UnsetType] = unset,
        created: Union[datetime, UnsetType] = unset,
        metadata: Union[NotebookMetadata, UnsetType] = unset,
        modified: Union[datetime, UnsetType] = unset,
        status: Union[NotebookStatus, UnsetType] = unset,
        **kwargs,
    ):
        """
        The attributes of a notebook.

        :param author: Attributes of user object returned by the API.
        :type author: NotebookAuthor, optional

        :param cells: List of cells to display in the notebook.
        :type cells: [NotebookCellResponse]

        :param created: UTC time stamp for when the notebook was created.
        :type created: datetime, optional

        :param metadata: Metadata associated with the notebook.
        :type metadata: NotebookMetadata, optional

        :param modified: UTC time stamp for when the notebook was last modified.
        :type modified: datetime, optional

        :param name: The name of the notebook.
        :type name: str

        :param status: Publication status of the notebook. For now, always "published".
        :type status: NotebookStatus, optional

        :param time: Notebook global timeframe.
        :type time: NotebookGlobalTime
        """
        if author is not unset:
            kwargs["author"] = author
        if created is not unset:
            kwargs["created"] = created
        if metadata is not unset:
            kwargs["metadata"] = metadata
        if modified is not unset:
            kwargs["modified"] = modified
        if status is not unset:
            kwargs["status"] = status
        super().__init__(kwargs)

        self_.cells = cells
        self_.name = name
        self_.time = time
