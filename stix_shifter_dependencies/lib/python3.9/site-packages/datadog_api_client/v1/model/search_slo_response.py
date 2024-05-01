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
    from datadog_api_client.v1.model.search_slo_response_data import SearchSLOResponseData
    from datadog_api_client.v1.model.search_slo_response_links import SearchSLOResponseLinks
    from datadog_api_client.v1.model.search_slo_response_meta import SearchSLOResponseMeta


class SearchSLOResponse(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.search_slo_response_data import SearchSLOResponseData
        from datadog_api_client.v1.model.search_slo_response_links import SearchSLOResponseLinks
        from datadog_api_client.v1.model.search_slo_response_meta import SearchSLOResponseMeta

        return {
            "data": (SearchSLOResponseData,),
            "links": (SearchSLOResponseLinks,),
            "meta": (SearchSLOResponseMeta,),
        }

    attribute_map = {
        "data": "data",
        "links": "links",
        "meta": "meta",
    }

    def __init__(
        self_,
        data: Union[SearchSLOResponseData, UnsetType] = unset,
        links: Union[SearchSLOResponseLinks, UnsetType] = unset,
        meta: Union[SearchSLOResponseMeta, UnsetType] = unset,
        **kwargs,
    ):
        """
        A search SLO response containing results from the search query.

        :param data: Data from search SLO response.
        :type data: SearchSLOResponseData, optional

        :param links: Pagination links.
        :type links: SearchSLOResponseLinks, optional

        :param meta: Searches metadata returned by the API.
        :type meta: SearchSLOResponseMeta, optional
        """
        if data is not unset:
            kwargs["data"] = data
        if links is not unset:
            kwargs["links"] = links
        if meta is not unset:
            kwargs["meta"] = meta
        super().__init__(kwargs)
