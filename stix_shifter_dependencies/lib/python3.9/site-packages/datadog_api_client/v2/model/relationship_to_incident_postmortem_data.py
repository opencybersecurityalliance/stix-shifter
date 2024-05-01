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
    from datadog_api_client.v2.model.incident_postmortem_type import IncidentPostmortemType


class RelationshipToIncidentPostmortemData(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.incident_postmortem_type import IncidentPostmortemType

        return {
            "id": (str,),
            "type": (IncidentPostmortemType,),
        }

    attribute_map = {
        "id": "id",
        "type": "type",
    }

    def __init__(self_, id: str, type: IncidentPostmortemType, **kwargs):
        """
        The postmortem relationship data.

        :param id: A unique identifier that represents the postmortem.
        :type id: str

        :param type: Incident postmortem resource type.
        :type type: IncidentPostmortemType
        """
        super().__init__(kwargs)

        self_.id = id
        self_.type = type
