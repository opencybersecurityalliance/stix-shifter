# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import List, Union, TYPE_CHECKING

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    none_type,
    unset,
    UnsetType,
)


if TYPE_CHECKING:
    from datadog_api_client.v1.model.shared_dashboard_update_request_global_time import (
        SharedDashboardUpdateRequestGlobalTime,
    )
    from datadog_api_client.v1.model.selectable_template_variable_items import SelectableTemplateVariableItems
    from datadog_api_client.v1.model.dashboard_share_type import DashboardShareType


class SharedDashboardUpdateRequest(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.shared_dashboard_update_request_global_time import (
            SharedDashboardUpdateRequestGlobalTime,
        )
        from datadog_api_client.v1.model.selectable_template_variable_items import SelectableTemplateVariableItems
        from datadog_api_client.v1.model.dashboard_share_type import DashboardShareType

        return {
            "global_time": (SharedDashboardUpdateRequestGlobalTime,),
            "global_time_selectable_enabled": (bool, none_type),
            "selectable_template_vars": ([SelectableTemplateVariableItems], none_type),
            "share_list": ([str], none_type),
            "share_type": (DashboardShareType,),
        }

    attribute_map = {
        "global_time": "global_time",
        "global_time_selectable_enabled": "global_time_selectable_enabled",
        "selectable_template_vars": "selectable_template_vars",
        "share_list": "share_list",
        "share_type": "share_type",
    }

    def __init__(
        self_,
        global_time: Union[SharedDashboardUpdateRequestGlobalTime, none_type],
        global_time_selectable_enabled: Union[bool, none_type, UnsetType] = unset,
        selectable_template_vars: Union[List[SelectableTemplateVariableItems], none_type, UnsetType] = unset,
        share_list: Union[List[str], none_type, UnsetType] = unset,
        share_type: Union[DashboardShareType, none_type, UnsetType] = unset,
        **kwargs,
    ):
        """
        Update a shared dashboard's settings.

        :param global_time: Timeframe setting for the shared dashboard.
        :type global_time: SharedDashboardUpdateRequestGlobalTime, none_type

        :param global_time_selectable_enabled: Whether to allow viewers to select a different global time setting for the shared dashboard.
        :type global_time_selectable_enabled: bool, none_type, optional

        :param selectable_template_vars: List of objects representing template variables on the shared dashboard which can have selectable values.
        :type selectable_template_vars: [SelectableTemplateVariableItems], none_type, optional

        :param share_list: List of email addresses that can be given access to the shared dashboard.
        :type share_list: [str], none_type, optional

        :param share_type: Type of sharing access (either open to anyone who has the public URL or invite-only).
        :type share_type: DashboardShareType, none_type, optional
        """
        if global_time_selectable_enabled is not unset:
            kwargs["global_time_selectable_enabled"] = global_time_selectable_enabled
        if selectable_template_vars is not unset:
            kwargs["selectable_template_vars"] = selectable_template_vars
        if share_list is not unset:
            kwargs["share_list"] = share_list
        if share_type is not unset:
            kwargs["share_type"] = share_type
        super().__init__(kwargs)

        self_.global_time = global_time
