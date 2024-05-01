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
    from datadog_api_client.v2.model.user_invitation_relationships import UserInvitationRelationships
    from datadog_api_client.v2.model.user_invitations_type import UserInvitationsType


class UserInvitationData(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.user_invitation_relationships import UserInvitationRelationships
        from datadog_api_client.v2.model.user_invitations_type import UserInvitationsType

        return {
            "relationships": (UserInvitationRelationships,),
            "type": (UserInvitationsType,),
        }

    attribute_map = {
        "relationships": "relationships",
        "type": "type",
    }

    def __init__(self_, relationships: UserInvitationRelationships, type: UserInvitationsType, **kwargs):
        """
        Object to create a user invitation.

        :param relationships: Relationships data for user invitation.
        :type relationships: UserInvitationRelationships

        :param type: User invitations type.
        :type type: UserInvitationsType
        """
        super().__init__(kwargs)

        self_.relationships = relationships
        self_.type = type
