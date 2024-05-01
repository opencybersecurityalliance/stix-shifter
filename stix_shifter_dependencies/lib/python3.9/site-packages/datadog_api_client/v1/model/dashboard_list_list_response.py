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
    from datadog_api_client.v1.model.dashboard_list import DashboardList


class DashboardListListResponse(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.dashboard_list import DashboardList

        return {
            "dashboard_lists": ([DashboardList],),
        }

    attribute_map = {
        "dashboard_lists": "dashboard_lists",
    }

    def __init__(self_, dashboard_lists: Union[List[DashboardList], UnsetType] = unset, **kwargs):
        """
        Information on your dashboard lists.

        :param dashboard_lists: List of all your dashboard lists.
        :type dashboard_lists: [DashboardList], optional
        """
        if dashboard_lists is not unset:
            kwargs["dashboard_lists"] = dashboard_lists
        super().__init__(kwargs)
