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
    from datadog_api_client.v2.model.incident_team_response_attributes import IncidentTeamResponseAttributes
    from datadog_api_client.v2.model.incident_team_relationships import IncidentTeamRelationships
    from datadog_api_client.v2.model.incident_team_type import IncidentTeamType


class IncidentTeamResponseData(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.incident_team_response_attributes import IncidentTeamResponseAttributes
        from datadog_api_client.v2.model.incident_team_relationships import IncidentTeamRelationships
        from datadog_api_client.v2.model.incident_team_type import IncidentTeamType

        return {
            "attributes": (IncidentTeamResponseAttributes,),
            "id": (str,),
            "relationships": (IncidentTeamRelationships,),
            "type": (IncidentTeamType,),
        }

    attribute_map = {
        "attributes": "attributes",
        "id": "id",
        "relationships": "relationships",
        "type": "type",
    }
    read_only_vars = {
        "relationships",
    }

    def __init__(
        self_,
        attributes: Union[IncidentTeamResponseAttributes, UnsetType] = unset,
        id: Union[str, UnsetType] = unset,
        relationships: Union[IncidentTeamRelationships, UnsetType] = unset,
        type: Union[IncidentTeamType, UnsetType] = unset,
        **kwargs,
    ):
        """
        Incident Team data from a response.

        :param attributes: The incident team's attributes from a response.
        :type attributes: IncidentTeamResponseAttributes, optional

        :param id: The incident team's ID.
        :type id: str, optional

        :param relationships: The incident team's relationships.
        :type relationships: IncidentTeamRelationships, optional

        :param type: Incident Team resource type.
        :type type: IncidentTeamType, optional
        """
        if attributes is not unset:
            kwargs["attributes"] = attributes
        if id is not unset:
            kwargs["id"] = id
        if relationships is not unset:
            kwargs["relationships"] = relationships
        if type is not unset:
            kwargs["type"] = type
        super().__init__(kwargs)
