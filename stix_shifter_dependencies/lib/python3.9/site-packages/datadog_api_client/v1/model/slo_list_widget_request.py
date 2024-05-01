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
    from datadog_api_client.v1.model.slo_list_widget_query import SLOListWidgetQuery
    from datadog_api_client.v1.model.slo_list_widget_request_type import SLOListWidgetRequestType


class SLOListWidgetRequest(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.slo_list_widget_query import SLOListWidgetQuery
        from datadog_api_client.v1.model.slo_list_widget_request_type import SLOListWidgetRequestType

        return {
            "query": (SLOListWidgetQuery,),
            "request_type": (SLOListWidgetRequestType,),
        }

    attribute_map = {
        "query": "query",
        "request_type": "request_type",
    }

    def __init__(self_, query: SLOListWidgetQuery, request_type: SLOListWidgetRequestType, **kwargs):
        """
        Updated SLO List widget.

        :param query: Updated SLO List widget.
        :type query: SLOListWidgetQuery

        :param request_type: Widget request type.
        :type request_type: SLOListWidgetRequestType
        """
        super().__init__(kwargs)

        self_.query = query
        self_.request_type = request_type
