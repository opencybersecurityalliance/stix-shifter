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
    from datadog_api_client.v1.model.shared_dashboard_invites_data import SharedDashboardInvitesData
    from datadog_api_client.v1.model.shared_dashboard_invites_meta import SharedDashboardInvitesMeta
    from datadog_api_client.v1.model.shared_dashboard_invites_data_object import SharedDashboardInvitesDataObject
    from datadog_api_client.v1.model.shared_dashboard_invites_data_list import SharedDashboardInvitesDataList


class SharedDashboardInvites(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.shared_dashboard_invites_data import SharedDashboardInvitesData
        from datadog_api_client.v1.model.shared_dashboard_invites_meta import SharedDashboardInvitesMeta

        return {
            "data": (SharedDashboardInvitesData,),
            "meta": (SharedDashboardInvitesMeta,),
        }

    attribute_map = {
        "data": "data",
        "meta": "meta",
    }
    read_only_vars = {
        "meta",
    }

    def __init__(
        self_,
        data: Union[SharedDashboardInvitesData, SharedDashboardInvitesDataObject, SharedDashboardInvitesDataList],
        meta: Union[SharedDashboardInvitesMeta, UnsetType] = unset,
        **kwargs,
    ):
        """
        Invitations data and metadata that exists for a shared dashboard returned by the API.

        :param data: An object or list of objects containing the information for an invitation to a shared dashboard.
        :type data: SharedDashboardInvitesData

        :param meta: Pagination metadata returned by the API.
        :type meta: SharedDashboardInvitesMeta, optional
        """
        if meta is not unset:
            kwargs["meta"] = meta
        super().__init__(kwargs)

        self_.data = data
