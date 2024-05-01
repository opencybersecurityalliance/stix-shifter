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
    from datadog_api_client.v2.model.nullable_relationship_to_user import NullableRelationshipToUser
    from datadog_api_client.v2.model.relationship_to_incident_integration_metadatas import (
        RelationshipToIncidentIntegrationMetadatas,
    )
    from datadog_api_client.v2.model.relationship_to_incident_postmortem import RelationshipToIncidentPostmortem


class IncidentUpdateRelationships(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.nullable_relationship_to_user import NullableRelationshipToUser
        from datadog_api_client.v2.model.relationship_to_incident_integration_metadatas import (
            RelationshipToIncidentIntegrationMetadatas,
        )
        from datadog_api_client.v2.model.relationship_to_incident_postmortem import RelationshipToIncidentPostmortem

        return {
            "commander_user": (NullableRelationshipToUser,),
            "integrations": (RelationshipToIncidentIntegrationMetadatas,),
            "postmortem": (RelationshipToIncidentPostmortem,),
        }

    attribute_map = {
        "commander_user": "commander_user",
        "integrations": "integrations",
        "postmortem": "postmortem",
    }

    def __init__(
        self_,
        commander_user: Union[NullableRelationshipToUser, UnsetType] = unset,
        integrations: Union[RelationshipToIncidentIntegrationMetadatas, UnsetType] = unset,
        postmortem: Union[RelationshipToIncidentPostmortem, UnsetType] = unset,
        **kwargs,
    ):
        """
        The incident's relationships for an update request.

        :param commander_user: Relationship to user.
        :type commander_user: NullableRelationshipToUser, optional

        :param integrations: A relationship reference for multiple integration metadata objects.
        :type integrations: RelationshipToIncidentIntegrationMetadatas, optional

        :param postmortem: A relationship reference for postmortems.
        :type postmortem: RelationshipToIncidentPostmortem, optional
        """
        if commander_user is not unset:
            kwargs["commander_user"] = commander_user
        if integrations is not unset:
            kwargs["integrations"] = integrations
        if postmortem is not unset:
            kwargs["postmortem"] = postmortem
        super().__init__(kwargs)
