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
    from datadog_api_client.v1.model.search_slo_response_meta_page import SearchSLOResponseMetaPage


class SearchSLOResponseMeta(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.search_slo_response_meta_page import SearchSLOResponseMetaPage

        return {
            "pagination": (SearchSLOResponseMetaPage,),
        }

    attribute_map = {
        "pagination": "pagination",
    }

    def __init__(self_, pagination: Union[SearchSLOResponseMetaPage, UnsetType] = unset, **kwargs):
        """
        Searches metadata returned by the API.

        :param pagination: Pagination metadata returned by the API.
        :type pagination: SearchSLOResponseMetaPage, optional
        """
        if pagination is not unset:
            kwargs["pagination"] = pagination
        super().__init__(kwargs)
