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
    from datadog_api_client.v2.model.relationship_to_incident_attachment import RelationshipToIncidentAttachment
    from datadog_api_client.v2.model.nullable_relationship_to_user import NullableRelationshipToUser
    from datadog_api_client.v2.model.relationship_to_user import RelationshipToUser
    from datadog_api_client.v2.model.relationship_to_incident_integration_metadatas import (
        RelationshipToIncidentIntegrationMetadatas,
    )


class IncidentResponseRelationships(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.relationship_to_incident_attachment import RelationshipToIncidentAttachment
        from datadog_api_client.v2.model.nullable_relationship_to_user import NullableRelationshipToUser
        from datadog_api_client.v2.model.relationship_to_user import RelationshipToUser
        from datadog_api_client.v2.model.relationship_to_incident_integration_metadatas import (
            RelationshipToIncidentIntegrationMetadatas,
        )

        return {
            "attachments": (RelationshipToIncidentAttachment,),
            "commander_user": (NullableRelationshipToUser,),
            "created_by_user": (RelationshipToUser,),
            "integrations": (RelationshipToIncidentIntegrationMetadatas,),
            "last_modified_by_user": (RelationshipToUser,),
        }

    attribute_map = {
        "attachments": "attachments",
        "commander_user": "commander_user",
        "created_by_user": "created_by_user",
        "integrations": "integrations",
        "last_modified_by_user": "last_modified_by_user",
    }

    def __init__(
        self_,
        attachments: Union[RelationshipToIncidentAttachment, UnsetType] = unset,
        commander_user: Union[NullableRelationshipToUser, UnsetType] = unset,
        created_by_user: Union[RelationshipToUser, UnsetType] = unset,
        integrations: Union[RelationshipToIncidentIntegrationMetadatas, UnsetType] = unset,
        last_modified_by_user: Union[RelationshipToUser, UnsetType] = unset,
        **kwargs,
    ):
        """
        The incident's relationships from a response.

        :param attachments: A relationship reference for attachments.
        :type attachments: RelationshipToIncidentAttachment, optional

        :param commander_user: Relationship to user.
        :type commander_user: NullableRelationshipToUser, optional

        :param created_by_user: Relationship to user.
        :type created_by_user: RelationshipToUser, optional

        :param integrations: A relationship reference for multiple integration metadata objects.
        :type integrations: RelationshipToIncidentIntegrationMetadatas, optional

        :param last_modified_by_user: Relationship to user.
        :type last_modified_by_user: RelationshipToUser, optional
        """
        if attachments is not unset:
            kwargs["attachments"] = attachments
        if commander_user is not unset:
            kwargs["commander_user"] = commander_user
        if created_by_user is not unset:
            kwargs["created_by_user"] = created_by_user
        if integrations is not unset:
            kwargs["integrations"] = integrations
        if last_modified_by_user is not unset:
            kwargs["last_modified_by_user"] = last_modified_by_user
        super().__init__(kwargs)
