# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelComposed,
    cached_property,
)


class TeamIncluded(ModelComposed):
    def __init__(self, **kwargs):
        """
        Included resources related to the team

        :param attributes: Attributes of user object returned by the API.
        :type attributes: UserAttributes, optional

        :param id: ID of the user.
        :type id: str, optional

        :param relationships: Relationships of the user object returned by the API.
        :type relationships: UserResponseRelationships, optional

        :param type: Users resource type.
        :type type: UsersType, optional
        """
        super().__init__(kwargs)

    @cached_property
    def _composed_schemas(_):
        # we need this here to make our import statements work
        # we must store _composed_schemas in here so the code is only run
        # when we invoke this method. If we kept this at the class
        # level we would get an error because the class level
        # code would be run when this module is imported, and these composed
        # classes don't exist yet because their module has not finished
        # loading
        from datadog_api_client.v2.model.user import User
        from datadog_api_client.v2.model.team_link import TeamLink
        from datadog_api_client.v2.model.user_team_permission import UserTeamPermission

        return {
            "oneOf": [
                User,
                TeamLink,
                UserTeamPermission,
            ],
        }
