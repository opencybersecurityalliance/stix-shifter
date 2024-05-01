# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelComposed,
    cached_property,
)


class SharedDashboardInvitesData(ModelComposed):
    def __init__(self, **kwargs):
        """
        An object or list of objects containing the information for an invitation to a shared dashboard.

        :param attributes: Attributes of the shared dashboard invitation
        :type attributes: SharedDashboardInvitesDataObjectAttributes

        :param type: Type for shared dashboard invitation request body.
        :type type: DashboardInviteType
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
        from datadog_api_client.v1.model.shared_dashboard_invites_data_object import SharedDashboardInvitesDataObject
        from datadog_api_client.v1.model.shared_dashboard_invites_data_list import SharedDashboardInvitesDataList

        return {
            "oneOf": [
                SharedDashboardInvitesDataObject,
                SharedDashboardInvitesDataList,
            ],
        }
