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
    from datadog_api_client.v1.model.dashboard_layout_type import DashboardLayoutType
    from datadog_api_client.v1.model.dashboard_reflow_type import DashboardReflowType
    from datadog_api_client.v1.model.dashboard_template_variable_preset import DashboardTemplateVariablePreset
    from datadog_api_client.v1.model.dashboard_template_variable import DashboardTemplateVariable
    from datadog_api_client.v1.model.widget import Widget


class Dashboard(ModelNormal):
    validations = {
        "tags": {
            "max_items": 5,
        },
    }

    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.dashboard_layout_type import DashboardLayoutType
        from datadog_api_client.v1.model.dashboard_reflow_type import DashboardReflowType
        from datadog_api_client.v1.model.dashboard_template_variable_preset import DashboardTemplateVariablePreset
        from datadog_api_client.v1.model.dashboard_template_variable import DashboardTemplateVariable
        from datadog_api_client.v1.model.widget import Widget

        return {
            "author_handle": (str,),
            "author_name": (str, none_type),
            "created_at": (datetime,),
            "description": (str, none_type),
            "id": (str,),
            "is_read_only": (bool,),
            "layout_type": (DashboardLayoutType,),
            "modified_at": (datetime,),
            "notify_list": ([str], none_type),
            "reflow_type": (DashboardReflowType,),
            "restricted_roles": ([str],),
            "tags": ([str], none_type),
            "template_variable_presets": ([DashboardTemplateVariablePreset], none_type),
            "template_variables": ([DashboardTemplateVariable], none_type),
            "title": (str,),
            "url": (str,),
            "widgets": ([Widget],),
        }

    attribute_map = {
        "author_handle": "author_handle",
        "author_name": "author_name",
        "created_at": "created_at",
        "description": "description",
        "id": "id",
        "is_read_only": "is_read_only",
        "layout_type": "layout_type",
        "modified_at": "modified_at",
        "notify_list": "notify_list",
        "reflow_type": "reflow_type",
        "restricted_roles": "restricted_roles",
        "tags": "tags",
        "template_variable_presets": "template_variable_presets",
        "template_variables": "template_variables",
        "title": "title",
        "url": "url",
        "widgets": "widgets",
    }
    read_only_vars = {
        "author_handle",
        "author_name",
        "created_at",
        "id",
        "modified_at",
        "url",
    }

    def __init__(
        self_,
        layout_type: DashboardLayoutType,
        title: str,
        widgets: List[Widget],
        author_handle: Union[str, UnsetType] = unset,
        author_name: Union[str, none_type, UnsetType] = unset,
        created_at: Union[datetime, UnsetType] = unset,
        description: Union[str, none_type, UnsetType] = unset,
        id: Union[str, UnsetType] = unset,
        is_read_only: Union[bool, UnsetType] = unset,
        modified_at: Union[datetime, UnsetType] = unset,
        notify_list: Union[List[str], none_type, UnsetType] = unset,
        reflow_type: Union[DashboardReflowType, UnsetType] = unset,
        restricted_roles: Union[List[str], UnsetType] = unset,
        tags: Union[List[str], none_type, UnsetType] = unset,
        template_variable_presets: Union[List[DashboardTemplateVariablePreset], none_type, UnsetType] = unset,
        template_variables: Union[List[DashboardTemplateVariable], none_type, UnsetType] = unset,
        url: Union[str, UnsetType] = unset,
        **kwargs,
    ):
        """
        A dashboard is Datadog’s tool for visually tracking, analyzing, and displaying
        key performance metrics, which enable you to monitor the health of your infrastructure.

        :param author_handle: Identifier of the dashboard author.
        :type author_handle: str, optional

        :param author_name: Name of the dashboard author.
        :type author_name: str, none_type, optional

        :param created_at: Creation date of the dashboard.
        :type created_at: datetime, optional

        :param description: Description of the dashboard.
        :type description: str, none_type, optional

        :param id: ID of the dashboard.
        :type id: str, optional

        :param is_read_only: Whether this dashboard is read-only. If True, only the author and admins can make changes to it. Prefer using ``restricted_roles`` to manage write authorization. **Deprecated**.
        :type is_read_only: bool, optional

        :param layout_type: Layout type of the dashboard.
        :type layout_type: DashboardLayoutType

        :param modified_at: Modification date of the dashboard.
        :type modified_at: datetime, optional

        :param notify_list: List of handles of users to notify when changes are made to this dashboard.
        :type notify_list: [str], none_type, optional

        :param reflow_type: Reflow type for a **new dashboard layout** dashboard. Set this only when layout type is 'ordered'.
            If set to 'fixed', the dashboard expects all widgets to have a layout, and if it's set to 'auto',
            widgets should not have layouts.
        :type reflow_type: DashboardReflowType, optional

        :param restricted_roles: A list of role identifiers. Only the author and users associated with at least one of these roles can edit this dashboard.
        :type restricted_roles: [str], optional

        :param tags: List of team names representing ownership of a dashboard.
        :type tags: [str], none_type, optional

        :param template_variable_presets: Array of template variables saved views.
        :type template_variable_presets: [DashboardTemplateVariablePreset], none_type, optional

        :param template_variables: List of template variables for this dashboard.
        :type template_variables: [DashboardTemplateVariable], none_type, optional

        :param title: Title of the dashboard.
        :type title: str

        :param url: The URL of the dashboard.
        :type url: str, optional

        :param widgets: List of widgets to display on the dashboard.
        :type widgets: [Widget]
        """
        if author_handle is not unset:
            kwargs["author_handle"] = author_handle
        if author_name is not unset:
            kwargs["author_name"] = author_name
        if created_at is not unset:
            kwargs["created_at"] = created_at
        if description is not unset:
            kwargs["description"] = description
        if id is not unset:
            kwargs["id"] = id
        if is_read_only is not unset:
            kwargs["is_read_only"] = is_read_only
        if modified_at is not unset:
            kwargs["modified_at"] = modified_at
        if notify_list is not unset:
            kwargs["notify_list"] = notify_list
        if reflow_type is not unset:
            kwargs["reflow_type"] = reflow_type
        if restricted_roles is not unset:
            kwargs["restricted_roles"] = restricted_roles
        if tags is not unset:
            kwargs["tags"] = tags
        if template_variable_presets is not unset:
            kwargs["template_variable_presets"] = template_variable_presets
        if template_variables is not unset:
            kwargs["template_variables"] = template_variables
        if url is not unset:
            kwargs["url"] = url
        super().__init__(kwargs)

        self_.layout_type = layout_type
        self_.title = title
        self_.widgets = widgets
