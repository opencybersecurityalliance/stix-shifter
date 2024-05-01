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
    from datadog_api_client.v2.model.incident_response_data import IncidentResponseData
    from datadog_api_client.v2.model.incident_response_included_item import IncidentResponseIncludedItem
    from datadog_api_client.v2.model.user import User
    from datadog_api_client.v2.model.incident_attachment_data import IncidentAttachmentData


class IncidentResponse(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.incident_response_data import IncidentResponseData
        from datadog_api_client.v2.model.incident_response_included_item import IncidentResponseIncludedItem

        return {
            "data": (IncidentResponseData,),
            "included": ([IncidentResponseIncludedItem],),
        }

    attribute_map = {
        "data": "data",
        "included": "included",
    }
    read_only_vars = {
        "included",
    }

    def __init__(
        self_,
        data: IncidentResponseData,
        included: Union[List[Union[IncidentResponseIncludedItem, User, IncidentAttachmentData]], UnsetType] = unset,
        **kwargs,
    ):
        """
        Response with an incident.

        :param data: Incident data from a response.
        :type data: IncidentResponseData

        :param included: Included related resources that the user requested.
        :type included: [IncidentResponseIncludedItem], optional
        """
        if included is not unset:
            kwargs["included"] = included
        super().__init__(kwargs)

        self_.data = data
