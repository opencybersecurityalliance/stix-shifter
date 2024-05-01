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
    from datadog_api_client.v2.model.incident_attachments_postmortem_attributes_attachment_object import (
        IncidentAttachmentsPostmortemAttributesAttachmentObject,
    )
    from datadog_api_client.v2.model.incident_attachment_postmortem_attachment_type import (
        IncidentAttachmentPostmortemAttachmentType,
    )


class IncidentAttachmentPostmortemAttributes(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.incident_attachments_postmortem_attributes_attachment_object import (
            IncidentAttachmentsPostmortemAttributesAttachmentObject,
        )
        from datadog_api_client.v2.model.incident_attachment_postmortem_attachment_type import (
            IncidentAttachmentPostmortemAttachmentType,
        )

        return {
            "attachment": (IncidentAttachmentsPostmortemAttributesAttachmentObject,),
            "attachment_type": (IncidentAttachmentPostmortemAttachmentType,),
        }

    attribute_map = {
        "attachment": "attachment",
        "attachment_type": "attachment_type",
    }

    def __init__(
        self_,
        attachment: IncidentAttachmentsPostmortemAttributesAttachmentObject,
        attachment_type: IncidentAttachmentPostmortemAttachmentType,
        **kwargs,
    ):
        """
        The attributes object for a postmortem attachment.

        :param attachment: The postmortem attachment.
        :type attachment: IncidentAttachmentsPostmortemAttributesAttachmentObject

        :param attachment_type: The type of postmortem attachment attributes.
        :type attachment_type: IncidentAttachmentPostmortemAttachmentType
        """
        super().__init__(kwargs)

        self_.attachment = attachment
        self_.attachment_type = attachment_type
