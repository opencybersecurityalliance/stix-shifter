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
    from datadog_api_client.v2.model.incident_attachment_type import IncidentAttachmentType


class RelationshipToIncidentAttachmentData(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.incident_attachment_type import IncidentAttachmentType

        return {
            "id": (str,),
            "type": (IncidentAttachmentType,),
        }

    attribute_map = {
        "id": "id",
        "type": "type",
    }

    def __init__(self_, id: str, type: IncidentAttachmentType, **kwargs):
        """
        The attachment relationship data.

        :param id: A unique identifier that represents the attachment.
        :type id: str

        :param type: The incident attachment resource type.
        :type type: IncidentAttachmentType
        """
        super().__init__(kwargs)

        self_.id = id
        self_.type = type
