# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelComposed,
    cached_property,
)


class IncidentTimelineCellCreateAttributes(ModelComposed):
    def __init__(self, **kwargs):
        """
        The timeline cell's attributes for a create request.

        :param cell_type: Type of the Markdown timeline cell.
        :type cell_type: IncidentTimelineCellMarkdownContentType

        :param content: The Markdown timeline cell contents.
        :type content: IncidentTimelineCellMarkdownCreateAttributesContent

        :param important: A flag indicating whether the timeline cell is important and should be highlighted.
        :type important: bool, optional
        """
        super().__init__(kwargs)

    @cached_property
    def _composed_schemas(_):
        # we need this here to make our import statements work
        # we must store _composed_schemas in here so the code is only run
        # when we invoke this method. If we kept this at the class
        # level we would get an error because the class level
        # code would be run when this module is imported, and these composed
        # classes don't exist yet because their module has not finished
        # loading
        from datadog_api_client.v2.model.incident_timeline_cell_markdown_create_attributes import (
            IncidentTimelineCellMarkdownCreateAttributes,
        )

        return {
            "oneOf": [
                IncidentTimelineCellMarkdownCreateAttributes,
            ],
        }
