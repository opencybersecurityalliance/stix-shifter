# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import List, Union, TYPE_CHECKING

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    unset,
    UnsetType,
)


if TYPE_CHECKING:
    from datadog_api_client.v2.model.dashboard_list_item_response import DashboardListItemResponse


class DashboardListAddItemsResponse(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.dashboard_list_item_response import DashboardListItemResponse

        return {
            "added_dashboards_to_list": ([DashboardListItemResponse],),
        }

    attribute_map = {
        "added_dashboards_to_list": "added_dashboards_to_list",
    }

    def __init__(self_, added_dashboards_to_list: Union[List[DashboardListItemResponse], UnsetType] = unset, **kwargs):
        """
        Response containing a list of added dashboards.

        :param added_dashboards_to_list: List of dashboards added to the dashboard list.
        :type added_dashboards_to_list: [DashboardListItemResponse], optional
        """
        if added_dashboards_to_list is not unset:
            kwargs["added_dashboards_to_list"] = added_dashboards_to_list
        super().__init__(kwargs)
