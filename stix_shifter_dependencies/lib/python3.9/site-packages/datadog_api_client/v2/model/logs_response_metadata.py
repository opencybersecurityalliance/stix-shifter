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
    from datadog_api_client.v2.model.logs_response_metadata_page import LogsResponseMetadataPage
    from datadog_api_client.v2.model.logs_aggregate_response_status import LogsAggregateResponseStatus
    from datadog_api_client.v2.model.logs_warning import LogsWarning


class LogsResponseMetadata(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.logs_response_metadata_page import LogsResponseMetadataPage
        from datadog_api_client.v2.model.logs_aggregate_response_status import LogsAggregateResponseStatus
        from datadog_api_client.v2.model.logs_warning import LogsWarning

        return {
            "elapsed": (int,),
            "page": (LogsResponseMetadataPage,),
            "request_id": (str,),
            "status": (LogsAggregateResponseStatus,),
            "warnings": ([LogsWarning],),
        }

    attribute_map = {
        "elapsed": "elapsed",
        "page": "page",
        "request_id": "request_id",
        "status": "status",
        "warnings": "warnings",
    }

    def __init__(
        self_,
        elapsed: Union[int, UnsetType] = unset,
        page: Union[LogsResponseMetadataPage, UnsetType] = unset,
        request_id: Union[str, UnsetType] = unset,
        status: Union[LogsAggregateResponseStatus, UnsetType] = unset,
        warnings: Union[List[LogsWarning], UnsetType] = unset,
        **kwargs,
    ):
        """
        The metadata associated with a request

        :param elapsed: The time elapsed in milliseconds
        :type elapsed: int, optional

        :param page: Paging attributes.
        :type page: LogsResponseMetadataPage, optional

        :param request_id: The identifier of the request
        :type request_id: str, optional

        :param status: The status of the response
        :type status: LogsAggregateResponseStatus, optional

        :param warnings: A list of warnings (non fatal errors) encountered, partial results might be returned if
            warnings are present in the response.
        :type warnings: [LogsWarning], optional
        """
        if elapsed is not unset:
            kwargs["elapsed"] = elapsed
        if page is not unset:
            kwargs["page"] = page
        if request_id is not unset:
            kwargs["request_id"] = request_id
        if status is not unset:
            kwargs["status"] = status
        if warnings is not unset:
            kwargs["warnings"] = warnings
        super().__init__(kwargs)
