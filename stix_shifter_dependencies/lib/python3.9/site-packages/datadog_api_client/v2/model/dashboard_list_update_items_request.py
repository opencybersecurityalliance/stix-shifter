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
    from datadog_api_client.v2.model.dashboard_list_item_request import DashboardListItemRequest


class DashboardListUpdateItemsRequest(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.dashboard_list_item_request import DashboardListItemRequest

        return {
            "dashboards": ([DashboardListItemRequest],),
        }

    attribute_map = {
        "dashboards": "dashboards",
    }

    def __init__(self_, dashboards: Union[List[DashboardListItemRequest], UnsetType] = unset, **kwargs):
        """
        Request containing the list of dashboards to update to.

        :param dashboards: List of dashboards to update the dashboard list to.
        :type dashboards: [DashboardListItemRequest], optional
        """
        if dashboards is not unset:
            kwargs["dashboards"] = dashboards
        super().__init__(kwargs)
