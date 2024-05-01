# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import List, Union, TYPE_CHECKING

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    unset,
    UnsetType,
)


if TYPE_CHECKING:
    from datadog_api_client.v2.model.incident_attachment_data import IncidentAttachmentData
    from datadog_api_client.v2.model.incident_attachments_response_included_item import (
        IncidentAttachmentsResponseIncludedItem,
    )
    from datadog_api_client.v2.model.user import User


class IncidentAttachmentUpdateResponse(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.incident_attachment_data import IncidentAttachmentData
        from datadog_api_client.v2.model.incident_attachments_response_included_item import (
            IncidentAttachmentsResponseIncludedItem,
        )

        return {
            "data": ([IncidentAttachmentData],),
            "included": ([IncidentAttachmentsResponseIncludedItem],),
        }

    attribute_map = {
        "data": "data",
        "included": "included",
    }

    def __init__(
        self_,
        data: List[IncidentAttachmentData],
        included: Union[List[Union[IncidentAttachmentsResponseIncludedItem, User]], UnsetType] = unset,
        **kwargs,
    ):
        """
        The response object containing the created or updated incident attachments.

        :param data: An array of incident attachments. Only the attachments that were created or updated by the request are
            returned.
        :type data: [IncidentAttachmentData]

        :param included: Included related resources that the user requested.
        :type included: [IncidentAttachmentsResponseIncludedItem], optional
        """
        if included is not unset:
            kwargs["included"] = included
        super().__init__(kwargs)

        self_.data = data
