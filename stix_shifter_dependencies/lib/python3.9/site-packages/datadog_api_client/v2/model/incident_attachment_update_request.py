# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import List, TYPE_CHECKING

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
)


if TYPE_CHECKING:
    from datadog_api_client.v2.model.incident_attachment_update_data import IncidentAttachmentUpdateData


class IncidentAttachmentUpdateRequest(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.incident_attachment_update_data import IncidentAttachmentUpdateData

        return {
            "data": ([IncidentAttachmentUpdateData],),
        }

    attribute_map = {
        "data": "data",
    }

    def __init__(self_, data: List[IncidentAttachmentUpdateData], **kwargs):
        """
        The update request for an incident's attachments.

        :param data: An array of incident attachments. An attachment object without an "id" key indicates that you want to
            create that attachment. An attachment object without an "attributes" key indicates that you want to
            delete that attachment. An attachment object with both the "id" key and a populated "attributes" object
            indicates that you want to update that attachment.
        :type data: [IncidentAttachmentUpdateData]
        """
        super().__init__(kwargs)

        self_.data = data
