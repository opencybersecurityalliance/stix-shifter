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
    from datadog_api_client.v2.model.incident_timeline_cell_markdown_content_type import (
        IncidentTimelineCellMarkdownContentType,
    )
    from datadog_api_client.v2.model.incident_timeline_cell_markdown_create_attributes_content import (
        IncidentTimelineCellMarkdownCreateAttributesContent,
    )


class IncidentTimelineCellMarkdownCreateAttributes(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.incident_timeline_cell_markdown_content_type import (
            IncidentTimelineCellMarkdownContentType,
        )
        from datadog_api_client.v2.model.incident_timeline_cell_markdown_create_attributes_content import (
            IncidentTimelineCellMarkdownCreateAttributesContent,
        )

        return {
            "cell_type": (IncidentTimelineCellMarkdownContentType,),
            "content": (IncidentTimelineCellMarkdownCreateAttributesContent,),
            "important": (bool,),
        }

    attribute_map = {
        "cell_type": "cell_type",
        "content": "content",
        "important": "important",
    }

    def __init__(
        self_,
        cell_type: IncidentTimelineCellMarkdownContentType,
        content: IncidentTimelineCellMarkdownCreateAttributesContent,
        important: Union[bool, UnsetType] = unset,
        **kwargs,
    ):
        """
        Timeline cell data for Markdown timeline cells for a create request.

        :param cell_type: Type of the Markdown timeline cell.
        :type cell_type: IncidentTimelineCellMarkdownContentType

        :param content: The Markdown timeline cell contents.
        :type content: IncidentTimelineCellMarkdownCreateAttributesContent

        :param important: A flag indicating whether the timeline cell is important and should be highlighted.
        :type important: bool, optional
        """
        if important is not unset:
            kwargs["important"] = important
        super().__init__(kwargs)

        self_.cell_type = cell_type
        self_.content = content
