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
    from datadog_api_client.v1.model.shared_dashboard_invites_meta_page import SharedDashboardInvitesMetaPage


class SharedDashboardInvitesMeta(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.shared_dashboard_invites_meta_page import SharedDashboardInvitesMetaPage

        return {
            "page": (SharedDashboardInvitesMetaPage,),
        }

    attribute_map = {
        "page": "page",
    }

    def __init__(self_, page: Union[SharedDashboardInvitesMetaPage, UnsetType] = unset, **kwargs):
        """
        Pagination metadata returned by the API.

        :param page: Object containing the total count of invitations across all pages
        :type page: SharedDashboardInvitesMetaPage, optional
        """
        if page is not unset:
            kwargs["page"] = page
        super().__init__(kwargs)
