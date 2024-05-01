# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import TYPE_CHECKING

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
)


if TYPE_CHECKING:
    from datadog_api_client.v1.model.notebooks_response_data_attributes import NotebooksResponseDataAttributes
    from datadog_api_client.v1.model.notebook_resource_type import NotebookResourceType


class NotebooksResponseData(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.notebooks_response_data_attributes import NotebooksResponseDataAttributes
        from datadog_api_client.v1.model.notebook_resource_type import NotebookResourceType

        return {
            "attributes": (NotebooksResponseDataAttributes,),
            "id": (int,),
            "type": (NotebookResourceType,),
        }

    attribute_map = {
        "attributes": "attributes",
        "id": "id",
        "type": "type",
    }
    read_only_vars = {
        "id",
    }

    def __init__(self_, attributes: NotebooksResponseDataAttributes, id: int, type: NotebookResourceType, **kwargs):
        """
        The data for a notebook in get all response.

        :param attributes: The attributes of a notebook in get all response.
        :type attributes: NotebooksResponseDataAttributes

        :param id: Unique notebook ID, assigned when you create the notebook.
        :type id: int

        :param type: Type of the Notebook resource.
        :type type: NotebookResourceType
        """
        super().__init__(kwargs)

        self_.attributes = attributes
        self_.id = id
        self_.type = type
