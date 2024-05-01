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
    from datadog_api_client.v2.model.incident_attachment_update_attributes import IncidentAttachmentUpdateAttributes
    from datadog_api_client.v2.model.incident_attachment_type import IncidentAttachmentType
    from datadog_api_client.v2.model.incident_attachment_postmortem_attributes import (
        IncidentAttachmentPostmortemAttributes,
    )
    from datadog_api_client.v2.model.incident_attachment_link_attributes import IncidentAttachmentLinkAttributes


class IncidentAttachmentUpdateData(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.incident_attachment_update_attributes import IncidentAttachmentUpdateAttributes
        from datadog_api_client.v2.model.incident_attachment_type import IncidentAttachmentType

        return {
            "attributes": (IncidentAttachmentUpdateAttributes,),
            "id": (str,),
            "type": (IncidentAttachmentType,),
        }

    attribute_map = {
        "attributes": "attributes",
        "id": "id",
        "type": "type",
    }

    def __init__(
        self_,
        type: IncidentAttachmentType,
        attributes: Union[
            IncidentAttachmentUpdateAttributes,
            IncidentAttachmentPostmortemAttributes,
            IncidentAttachmentLinkAttributes,
            UnsetType,
        ] = unset,
        id: Union[str, UnsetType] = unset,
        **kwargs,
    ):
        """
        A single incident attachment.

        :param attributes: Incident attachment attributes.
        :type attributes: IncidentAttachmentUpdateAttributes, optional

        :param id: A unique identifier that represents the incident attachment.
        :type id: str, optional

        :param type: The incident attachment resource type.
        :type type: IncidentAttachmentType
        """
        if attributes is not unset:
            kwargs["attributes"] = attributes
        if id is not unset:
            kwargs["id"] = id
        super().__init__(kwargs)

        self_.type = type
