# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import TYPE_CHECKING

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
)


if TYPE_CHECKING:
    from datadog_api_client.v1.model.dashboard_bulk_action_data_list import DashboardBulkActionDataList


class DashboardBulkDeleteRequest(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.dashboard_bulk_action_data_list import DashboardBulkActionDataList

        return {
            "data": (DashboardBulkActionDataList,),
        }

    attribute_map = {
        "data": "data",
    }

    def __init__(self_, data: DashboardBulkActionDataList, **kwargs):
        """
        Dashboard bulk delete request body.

        :param data: List of dashboard bulk action request data objects.
        :type data: DashboardBulkActionDataList
        """
        super().__init__(kwargs)

        self_.data = data
