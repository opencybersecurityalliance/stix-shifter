# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import List, TYPE_CHECKING

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
)


if TYPE_CHECKING:
    from datadog_api_client.v1.model.list_stream_column import ListStreamColumn
    from datadog_api_client.v1.model.list_stream_query import ListStreamQuery
    from datadog_api_client.v1.model.list_stream_response_format import ListStreamResponseFormat


class ListStreamWidgetRequest(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.list_stream_column import ListStreamColumn
        from datadog_api_client.v1.model.list_stream_query import ListStreamQuery
        from datadog_api_client.v1.model.list_stream_response_format import ListStreamResponseFormat

        return {
            "columns": ([ListStreamColumn],),
            "query": (ListStreamQuery,),
            "response_format": (ListStreamResponseFormat,),
        }

    attribute_map = {
        "columns": "columns",
        "query": "query",
        "response_format": "response_format",
    }

    def __init__(
        self_,
        columns: List[ListStreamColumn],
        query: ListStreamQuery,
        response_format: ListStreamResponseFormat,
        **kwargs,
    ):
        """
        Updated list stream widget.

        :param columns: Widget columns.
        :type columns: [ListStreamColumn]

        :param query: Updated list stream widget.
        :type query: ListStreamQuery

        :param response_format: Widget response format.
        :type response_format: ListStreamResponseFormat
        """
        super().__init__(kwargs)

        self_.columns = columns
        self_.query = query
        self_.response_format = response_format
