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
    from datadog_api_client.v2.model.relationship_to_organization import RelationshipToOrganization
    from datadog_api_client.v2.model.relationship_to_organizations import RelationshipToOrganizations
    from datadog_api_client.v2.model.relationship_to_users import RelationshipToUsers
    from datadog_api_client.v2.model.relationship_to_roles import RelationshipToRoles


class UserResponseRelationships(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.relationship_to_organization import RelationshipToOrganization
        from datadog_api_client.v2.model.relationship_to_organizations import RelationshipToOrganizations
        from datadog_api_client.v2.model.relationship_to_users import RelationshipToUsers
        from datadog_api_client.v2.model.relationship_to_roles import RelationshipToRoles

        return {
            "org": (RelationshipToOrganization,),
            "other_orgs": (RelationshipToOrganizations,),
            "other_users": (RelationshipToUsers,),
            "roles": (RelationshipToRoles,),
        }

    attribute_map = {
        "org": "org",
        "other_orgs": "other_orgs",
        "other_users": "other_users",
        "roles": "roles",
    }

    def __init__(
        self_,
        org: Union[RelationshipToOrganization, UnsetType] = unset,
        other_orgs: Union[RelationshipToOrganizations, UnsetType] = unset,
        other_users: Union[RelationshipToUsers, UnsetType] = unset,
        roles: Union[RelationshipToRoles, UnsetType] = unset,
        **kwargs,
    ):
        """
        Relationships of the user object returned by the API.

        :param org: Relationship to an organization.
        :type org: RelationshipToOrganization, optional

        :param other_orgs: Relationship to organizations.
        :type other_orgs: RelationshipToOrganizations, optional

        :param other_users: Relationship to users.
        :type other_users: RelationshipToUsers, optional

        :param roles: Relationship to roles.
        :type roles: RelationshipToRoles, optional
        """
        if org is not unset:
            kwargs["org"] = org
        if other_orgs is not unset:
            kwargs["other_orgs"] = other_orgs
        if other_users is not unset:
            kwargs["other_users"] = other_users
        if roles is not unset:
            kwargs["roles"] = roles
        super().__init__(kwargs)
