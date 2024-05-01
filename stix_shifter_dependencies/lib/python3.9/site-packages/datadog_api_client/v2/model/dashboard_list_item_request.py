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
    from datadog_api_client.v2.model.dashboard_type import DashboardType


class DashboardListItemRequest(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.dashboard_type import DashboardType

        return {
            "id": (str,),
            "type": (DashboardType,),
        }

    attribute_map = {
        "id": "id",
        "type": "type",
    }

    def __init__(self_, id: str, type: DashboardType, **kwargs):
        """
        A dashboard within a list.

        :param id: ID of the dashboard.
        :type id: str

        :param type: The type of the dashboard.
        :type type: DashboardType
        """
        super().__init__(kwargs)

        self_.id = id
        self_.type = type
