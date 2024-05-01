# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Union, TYPE_CHECKING

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
)


if TYPE_CHECKING:
    from datadog_api_client.v2.model.incident_attachment_attributes import IncidentAttachmentAttributes
    from datadog_api_client.v2.model.incident_attachment_relationships import IncidentAttachmentRelationships
    from datadog_api_client.v2.model.incident_attachment_type import IncidentAttachmentType
    from datadog_api_client.v2.model.incident_attachment_postmortem_attributes import (
        IncidentAttachmentPostmortemAttributes,
    )
    from datadog_api_client.v2.model.incident_attachment_link_attributes import IncidentAttachmentLinkAttributes


class IncidentAttachmentData(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.incident_attachment_attributes import IncidentAttachmentAttributes
        from datadog_api_client.v2.model.incident_attachment_relationships import IncidentAttachmentRelationships
        from datadog_api_client.v2.model.incident_attachment_type import IncidentAttachmentType

        return {
            "attributes": (IncidentAttachmentAttributes,),
            "id": (str,),
            "relationships": (IncidentAttachmentRelationships,),
            "type": (IncidentAttachmentType,),
        }

    attribute_map = {
        "attributes": "attributes",
        "id": "id",
        "relationships": "relationships",
        "type": "type",
    }

    def __init__(
        self_,
        attributes: Union[
            IncidentAttachmentAttributes, IncidentAttachmentPostmortemAttributes, IncidentAttachmentLinkAttributes
        ],
        id: str,
        relationships: IncidentAttachmentRelationships,
        type: IncidentAttachmentType,
        **kwargs,
    ):
        """
        A single incident attachment.

        :param attributes: The attributes object for an attachment.
        :type attributes: IncidentAttachmentAttributes

        :param id: A unique identifier that represents the incident attachment.
        :type id: str

        :param relationships: The incident attachment's relationships.
        :type relationships: IncidentAttachmentRelationships

        :param type: The incident attachment resource type.
        :type type: IncidentAttachmentType
        """
        super().__init__(kwargs)

        self_.attributes = attributes
        self_.id = id
        self_.relationships = relationships
        self_.type = type
