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
    from datadog_api_client.v2.model.incident_create_attributes import IncidentCreateAttributes
    from datadog_api_client.v2.model.incident_create_relationships import IncidentCreateRelationships
    from datadog_api_client.v2.model.incident_type import IncidentType


class IncidentCreateData(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.incident_create_attributes import IncidentCreateAttributes
        from datadog_api_client.v2.model.incident_create_relationships import IncidentCreateRelationships
        from datadog_api_client.v2.model.incident_type import IncidentType

        return {
            "attributes": (IncidentCreateAttributes,),
            "relationships": (IncidentCreateRelationships,),
            "type": (IncidentType,),
        }

    attribute_map = {
        "attributes": "attributes",
        "relationships": "relationships",
        "type": "type",
    }

    def __init__(
        self_,
        attributes: IncidentCreateAttributes,
        type: IncidentType,
        relationships: Union[IncidentCreateRelationships, UnsetType] = unset,
        **kwargs,
    ):
        """
        Incident data for a create request.

        :param attributes: The incident's attributes for a create request.
        :type attributes: IncidentCreateAttributes

        :param relationships: The relationships the incident will have with other resources once created.
        :type relationships: IncidentCreateRelationships, optional

        :param type: Incident resource type.
        :type type: IncidentType
        """
        if relationships is not unset:
            kwargs["relationships"] = relationships
        super().__init__(kwargs)

        self_.attributes = attributes
        self_.type = type
