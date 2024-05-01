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


class DashboardListUpdateItemsResponse(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.dashboard_list_item_response import DashboardListItemResponse

        return {
            "dashboards": ([DashboardListItemResponse],),
        }

    attribute_map = {
        "dashboards": "dashboards",
    }

    def __init__(self_, dashboards: Union[List[DashboardListItemResponse], UnsetType] = unset, **kwargs):
        """
        Response containing a list of updated dashboards.

        :param dashboards: List of dashboards in the dashboard list.
        :type dashboards: [DashboardListItemResponse], optional
        """
        if dashboards is not unset:
            kwargs["dashboards"] = dashboards
        super().__init__(kwargs)
