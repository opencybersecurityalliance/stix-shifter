# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Union, TYPE_CHECKING

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    datetime,
    unset,
    UnsetType,
)


if TYPE_CHECKING:
    from datadog_api_client.v1.model.creator import Creator


class DashboardList(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.creator import Creator

        return {
            "author": (Creator,),
            "created": (datetime,),
            "dashboard_count": (int,),
            "id": (int,),
            "is_favorite": (bool,),
            "modified": (datetime,),
            "name": (str,),
            "type": (str,),
        }

    attribute_map = {
        "author": "author",
        "created": "created",
        "dashboard_count": "dashboard_count",
        "id": "id",
        "is_favorite": "is_favorite",
        "modified": "modified",
        "name": "name",
        "type": "type",
    }
    read_only_vars = {
        "author",
        "created",
        "dashboard_count",
        "id",
        "is_favorite",
        "modified",
        "type",
    }

    def __init__(
        self_,
        name: str,
        author: Union[Creator, UnsetType] = unset,
        created: Union[datetime, UnsetType] = unset,
        dashboard_count: Union[int, UnsetType] = unset,
        id: Union[int, UnsetType] = unset,
        is_favorite: Union[bool, UnsetType] = unset,
        modified: Union[datetime, UnsetType] = unset,
        type: Union[str, UnsetType] = unset,
        **kwargs,
    ):
        """
        Your Datadog Dashboards.

        :param author: Object describing the creator of the shared element.
        :type author: Creator, optional

        :param created: Date of creation of the dashboard list.
        :type created: datetime, optional

        :param dashboard_count: The number of dashboards in the list.
        :type dashboard_count: int, optional

        :param id: The ID of the dashboard list.
        :type id: int, optional

        :param is_favorite: Whether or not the list is in the favorites.
        :type is_favorite: bool, optional

        :param modified: Date of last edition of the dashboard list.
        :type modified: datetime, optional

        :param name: The name of the dashboard list.
        :type name: str

        :param type: The type of dashboard list.
        :type type: str, optional
        """
        if author is not unset:
            kwargs["author"] = author
        if created is not unset:
            kwargs["created"] = created
        if dashboard_count is not unset:
            kwargs["dashboard_count"] = dashboard_count
        if id is not unset:
            kwargs["id"] = id
        if is_favorite is not unset:
            kwargs["is_favorite"] = is_favorite
        if modified is not unset:
            kwargs["modified"] = modified
        if type is not unset:
            kwargs["type"] = type
        super().__init__(kwargs)

        self_.name = name
