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
    from datadog_api_client.v2.model.incident_team_create_attributes import IncidentTeamCreateAttributes
    from datadog_api_client.v2.model.incident_team_relationships import IncidentTeamRelationships
    from datadog_api_client.v2.model.incident_team_type import IncidentTeamType


class IncidentTeamCreateData(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.incident_team_create_attributes import IncidentTeamCreateAttributes
        from datadog_api_client.v2.model.incident_team_relationships import IncidentTeamRelationships
        from datadog_api_client.v2.model.incident_team_type import IncidentTeamType

        return {
            "attributes": (IncidentTeamCreateAttributes,),
            "relationships": (IncidentTeamRelationships,),
            "type": (IncidentTeamType,),
        }

    attribute_map = {
        "attributes": "attributes",
        "relationships": "relationships",
        "type": "type",
    }
    read_only_vars = {
        "relationships",
    }

    def __init__(
        self_,
        type: IncidentTeamType,
        attributes: Union[IncidentTeamCreateAttributes, UnsetType] = unset,
        relationships: Union[IncidentTeamRelationships, UnsetType] = unset,
        **kwargs,
    ):
        """
        Incident Team data for a create request.

        :param attributes: The incident team's attributes for a create request.
        :type attributes: IncidentTeamCreateAttributes, optional

        :param relationships: The incident team's relationships.
        :type relationships: IncidentTeamRelationships, optional

        :param type: Incident Team resource type.
        :type type: IncidentTeamType
        """
        if attributes is not unset:
            kwargs["attributes"] = attributes
        if relationships is not unset:
            kwargs["relationships"] = relationships
        super().__init__(kwargs)

        self_.type = type
