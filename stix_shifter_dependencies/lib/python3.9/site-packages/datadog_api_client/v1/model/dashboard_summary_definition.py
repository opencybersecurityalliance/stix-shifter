# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Union, TYPE_CHECKING

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


class DashboardSummaryDefinition(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.dashboard_layout_type import DashboardLayoutType

        return {
            "author_handle": (str,),
            "created_at": (datetime,),
            "description": (str, none_type),
            "id": (str,),
            "is_read_only": (bool,),
            "layout_type": (DashboardLayoutType,),
            "modified_at": (datetime,),
            "title": (str,),
            "url": (str,),
        }

    attribute_map = {
        "author_handle": "author_handle",
        "created_at": "created_at",
        "description": "description",
        "id": "id",
        "is_read_only": "is_read_only",
        "layout_type": "layout_type",
        "modified_at": "modified_at",
        "title": "title",
        "url": "url",
    }

    def __init__(
        self_,
        author_handle: Union[str, UnsetType] = unset,
        created_at: Union[datetime, UnsetType] = unset,
        description: Union[str, none_type, UnsetType] = unset,
        id: Union[str, UnsetType] = unset,
        is_read_only: Union[bool, UnsetType] = unset,
        layout_type: Union[DashboardLayoutType, UnsetType] = unset,
        modified_at: Union[datetime, UnsetType] = unset,
        title: Union[str, UnsetType] = unset,
        url: Union[str, UnsetType] = unset,
        **kwargs,
    ):
        """
        Dashboard definition.

        :param author_handle: Identifier of the dashboard author.
        :type author_handle: str, optional

        :param created_at: Creation date of the dashboard.
        :type created_at: datetime, optional

        :param description: Description of the dashboard.
        :type description: str, none_type, optional

        :param id: Dashboard identifier.
        :type id: str, optional

        :param is_read_only: Whether this dashboard is read-only. If True, only the author and admins can make changes to it.
        :type is_read_only: bool, optional

        :param layout_type: Layout type of the dashboard.
        :type layout_type: DashboardLayoutType, optional

        :param modified_at: Modification date of the dashboard.
        :type modified_at: datetime, optional

        :param title: Title of the dashboard.
        :type title: str, optional

        :param url: URL of the dashboard.
        :type url: str, optional
        """
        if author_handle is not unset:
            kwargs["author_handle"] = author_handle
        if created_at is not unset:
            kwargs["created_at"] = created_at
        if description is not unset:
            kwargs["description"] = description
        if id is not unset:
            kwargs["id"] = id
        if is_read_only is not unset:
            kwargs["is_read_only"] = is_read_only
        if layout_type is not unset:
            kwargs["layout_type"] = layout_type
        if modified_at is not unset:
            kwargs["modified_at"] = modified_at
        if title is not unset:
            kwargs["title"] = title
        if url is not unset:
            kwargs["url"] = url
        super().__init__(kwargs)
