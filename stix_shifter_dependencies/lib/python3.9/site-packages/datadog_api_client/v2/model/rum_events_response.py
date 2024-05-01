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
    from datadog_api_client.v2.model.rum_event import RUMEvent
    from datadog_api_client.v2.model.rum_response_links import RUMResponseLinks
    from datadog_api_client.v2.model.rum_response_metadata import RUMResponseMetadata


class RUMEventsResponse(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.rum_event import RUMEvent
        from datadog_api_client.v2.model.rum_response_links import RUMResponseLinks
        from datadog_api_client.v2.model.rum_response_metadata import RUMResponseMetadata

        return {
            "data": ([RUMEvent],),
            "links": (RUMResponseLinks,),
            "meta": (RUMResponseMetadata,),
        }

    attribute_map = {
        "data": "data",
        "links": "links",
        "meta": "meta",
    }

    def __init__(
        self_,
        data: Union[List[RUMEvent], UnsetType] = unset,
        links: Union[RUMResponseLinks, UnsetType] = unset,
        meta: Union[RUMResponseMetadata, UnsetType] = unset,
        **kwargs,
    ):
        """
        Response object with all events matching the request and pagination information.

        :param data: Array of events matching the request.
        :type data: [RUMEvent], optional

        :param links: Links attributes.
        :type links: RUMResponseLinks, optional

        :param meta: The metadata associated with a request.
        :type meta: RUMResponseMetadata, optional
        """
        if data is not unset:
            kwargs["data"] = data
        if links is not unset:
            kwargs["links"] = links
        if meta is not unset:
            kwargs["meta"] = meta
        super().__init__(kwargs)
