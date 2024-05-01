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
    from datadog_api_client.v1.model.notebook_markdown_cell_definition_type import NotebookMarkdownCellDefinitionType


class NotebookMarkdownCellDefinition(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.notebook_markdown_cell_definition_type import (
            NotebookMarkdownCellDefinitionType,
        )

        return {
            "text": (str,),
            "type": (NotebookMarkdownCellDefinitionType,),
        }

    attribute_map = {
        "text": "text",
        "type": "type",
    }

    def __init__(self_, text: str, type: NotebookMarkdownCellDefinitionType, **kwargs):
        """
        Text in a notebook is formatted with `Markdown <https://daringfireball.net/projects/markdown/>`_ , which enables the use of headings, subheadings, links, images, lists, and code blocks.

        :param text: The markdown content.
        :type text: str

        :param type: Type of the markdown cell.
        :type type: NotebookMarkdownCellDefinitionType
        """
        super().__init__(kwargs)

        self_.text = text
        self_.type = type
