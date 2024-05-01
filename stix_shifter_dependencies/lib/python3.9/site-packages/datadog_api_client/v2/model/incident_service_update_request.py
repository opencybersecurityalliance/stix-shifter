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
    from datadog_api_client.v2.model.incident_service_update_data import IncidentServiceUpdateData


class IncidentServiceUpdateRequest(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.incident_service_update_data import IncidentServiceUpdateData

        return {
            "data": (IncidentServiceUpdateData,),
        }

    attribute_map = {
        "data": "data",
    }

    def __init__(self_, data: IncidentServiceUpdateData, **kwargs):
        """
        Update request with an incident service payload.

        :param data: Incident Service payload for update requests.
        :type data: IncidentServiceUpdateData
        """
        super().__init__(kwargs)

        self_.data = data
