# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Union, TYPE_CHECKING

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    unset,
    UnsetType,
)


if TYPE_CHECKING:
    from datadog_api_client.v1.model.topology_query import TopologyQuery
    from datadog_api_client.v1.model.topology_request_type import TopologyRequestType


class TopologyRequest(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.topology_query import TopologyQuery
        from datadog_api_client.v1.model.topology_request_type import TopologyRequestType

        return {
            "query": (TopologyQuery,),
            "request_type": (TopologyRequestType,),
        }

    attribute_map = {
        "query": "query",
        "request_type": "request_type",
    }

    def __init__(
        self_,
        query: Union[TopologyQuery, UnsetType] = unset,
        request_type: Union[TopologyRequestType, UnsetType] = unset,
        **kwargs,
    ):
        """
        Request that will return nodes and edges to be used by topology map.

        :param query: Query to service-based topology data sources like the service map or data streams.
        :type query: TopologyQuery, optional

        :param request_type: Widget request type.
        :type request_type: TopologyRequestType, optional
        """
        if query is not unset:
            kwargs["query"] = query
        if request_type is not unset:
            kwargs["request_type"] = request_type
        super().__init__(kwargs)
