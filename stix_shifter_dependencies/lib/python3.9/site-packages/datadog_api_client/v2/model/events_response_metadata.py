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
    from datadog_api_client.v2.model.events_response_metadata_page import EventsResponseMetadataPage
    from datadog_api_client.v2.model.events_warning import EventsWarning


class EventsResponseMetadata(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.events_response_metadata_page import EventsResponseMetadataPage
        from datadog_api_client.v2.model.events_warning import EventsWarning

        return {
            "elapsed": (int,),
            "page": (EventsResponseMetadataPage,),
            "request_id": (str,),
            "warnings": ([EventsWarning],),
        }

    attribute_map = {
        "elapsed": "elapsed",
        "page": "page",
        "request_id": "request_id",
        "warnings": "warnings",
    }

    def __init__(
        self_,
        elapsed: Union[int, UnsetType] = unset,
        page: Union[EventsResponseMetadataPage, UnsetType] = unset,
        request_id: Union[str, UnsetType] = unset,
        warnings: Union[List[EventsWarning], UnsetType] = unset,
        **kwargs,
    ):
        """
        The metadata associated with a request.

        :param elapsed: The time elapsed in milliseconds.
        :type elapsed: int, optional

        :param page: Pagination attributes.
        :type page: EventsResponseMetadataPage, optional

        :param request_id: The identifier of the request.
        :type request_id: str, optional

        :param warnings: A list of warnings (non-fatal errors) encountered. Partial results might be returned if
            warnings are present in the response.
        :type warnings: [EventsWarning], optional
        """
        if elapsed is not unset:
            kwargs["elapsed"] = elapsed
        if page is not unset:
            kwargs["page"] = page
        if request_id is not unset:
            kwargs["request_id"] = request_id
        if warnings is not unset:
            kwargs["warnings"] = warnings
        super().__init__(kwargs)
