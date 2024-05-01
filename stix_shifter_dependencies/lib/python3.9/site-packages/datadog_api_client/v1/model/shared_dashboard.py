# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import List, Union, TYPE_CHECKING

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    datetime,
    none_type,
    unset,
    UnsetType,
)


if TYPE_CHECKING:
    from datadog_api_client.v1.model.shared_dashboard_author import SharedDashboardAuthor
    from datadog_api_client.v1.model.dashboard_type import DashboardType
    from datadog_api_client.v1.model.dashboard_global_time import DashboardGlobalTime
    from datadog_api_client.v1.model.selectable_template_variable_items import SelectableTemplateVariableItems
    from datadog_api_client.v1.model.dashboard_share_type import DashboardShareType


class SharedDashboard(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.shared_dashboard_author import SharedDashboardAuthor
        from datadog_api_client.v1.model.dashboard_type import DashboardType
        from datadog_api_client.v1.model.dashboard_global_time import DashboardGlobalTime
        from datadog_api_client.v1.model.selectable_template_variable_items import SelectableTemplateVariableItems
        from datadog_api_client.v1.model.dashboard_share_type import DashboardShareType

        return {
            "author": (SharedDashboardAuthor,),
            "created_at": (datetime,),
            "dashboard_id": (str,),
            "dashboard_type": (DashboardType,),
            "global_time": (DashboardGlobalTime,),
            "global_time_selectable_enabled": (bool, none_type),
            "public_url": (str,),
            "selectable_template_vars": ([SelectableTemplateVariableItems], none_type),
            "share_list": ([str], none_type),
            "share_type": (DashboardShareType,),
            "token": (str,),
        }

    attribute_map = {
        "author": "author",
        "created_at": "created_at",
        "dashboard_id": "dashboard_id",
        "dashboard_type": "dashboard_type",
        "global_time": "global_time",
        "global_time_selectable_enabled": "global_time_selectable_enabled",
        "public_url": "public_url",
        "selectable_template_vars": "selectable_template_vars",
        "share_list": "share_list",
        "share_type": "share_type",
        "token": "token",
    }
    read_only_vars = {
        "author",
        "created_at",
        "public_url",
        "token",
    }

    def __init__(
        self_,
        dashboard_id: str,
        dashboard_type: DashboardType,
        author: Union[SharedDashboardAuthor, UnsetType] = unset,
        created_at: Union[datetime, UnsetType] = unset,
        global_time: Union[DashboardGlobalTime, UnsetType] = unset,
        global_time_selectable_enabled: Union[bool, none_type, UnsetType] = unset,
        public_url: Union[str, UnsetType] = unset,
        selectable_template_vars: Union[List[SelectableTemplateVariableItems], none_type, UnsetType] = unset,
        share_list: Union[List[str], none_type, UnsetType] = unset,
        share_type: Union[DashboardShareType, none_type, UnsetType] = unset,
        token: Union[str, UnsetType] = unset,
        **kwargs,
    ):
        """
        The metadata object associated with how a dashboard has been/will be shared.

        :param author: User who shared the dashboard.
        :type author: SharedDashboardAuthor, optional

        :param created_at: Date the dashboard was shared.
        :type created_at: datetime, optional

        :param dashboard_id: ID of the dashboard to share.
        :type dashboard_id: str

        :param dashboard_type: The type of the associated private dashboard.
        :type dashboard_type: DashboardType

        :param global_time: Object containing the live span selection for the dashboard.
        :type global_time: DashboardGlobalTime, optional

        :param global_time_selectable_enabled: Whether to allow viewers to select a different global time setting for the shared dashboard.
        :type global_time_selectable_enabled: bool, none_type, optional

        :param public_url: URL of the shared dashboard.
        :type public_url: str, optional

        :param selectable_template_vars: List of objects representing template variables on the shared dashboard which can have selectable values.
        :type selectable_template_vars: [SelectableTemplateVariableItems], none_type, optional

        :param share_list: List of email addresses that can receive an invitation to access to the shared dashboard.
        :type share_list: [str], none_type, optional

        :param share_type: Type of sharing access (either open to anyone who has the public URL or invite-only).
        :type share_type: DashboardShareType, none_type, optional

        :param token: A unique token assigned to the shared dashboard.
        :type token: str, optional
        """
        if author is not unset:
            kwargs["author"] = author
        if created_at is not unset:
            kwargs["created_at"] = created_at
        if global_time is not unset:
            kwargs["global_time"] = global_time
        if global_time_selectable_enabled is not unset:
            kwargs["global_time_selectable_enabled"] = global_time_selectable_enabled
        if public_url is not unset:
            kwargs["public_url"] = public_url
        if selectable_template_vars is not unset:
            kwargs["selectable_template_vars"] = selectable_template_vars
        if share_list is not unset:
            kwargs["share_list"] = share_list
        if share_type is not unset:
            kwargs["share_type"] = share_type
        if token is not unset:
            kwargs["token"] = token
        super().__init__(kwargs)

        self_.dashboard_id = dashboard_id
        self_.dashboard_type = dashboard_type
