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
    from datadog_api_client.v1.model.search_slo_response_data_attributes_facets import (
        SearchSLOResponseDataAttributesFacets,
    )
    from datadog_api_client.v1.model.search_service_level_objective import SearchServiceLevelObjective


class SearchSLOResponseDataAttributes(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.search_slo_response_data_attributes_facets import (
            SearchSLOResponseDataAttributesFacets,
        )
        from datadog_api_client.v1.model.search_service_level_objective import SearchServiceLevelObjective

        return {
            "facets": (SearchSLOResponseDataAttributesFacets,),
            "slos": ([SearchServiceLevelObjective],),
        }

    attribute_map = {
        "facets": "facets",
        "slos": "slos",
    }

    def __init__(
        self_,
        facets: Union[SearchSLOResponseDataAttributesFacets, UnsetType] = unset,
        slos: Union[List[SearchServiceLevelObjective], UnsetType] = unset,
        **kwargs,
    ):
        """
        Attributes

        :param facets: Facets
        :type facets: SearchSLOResponseDataAttributesFacets, optional

        :param slos: SLOs
        :type slos: [SearchServiceLevelObjective], optional
        """
        if facets is not unset:
            kwargs["facets"] = facets
        if slos is not unset:
            kwargs["slos"] = slos
        super().__init__(kwargs)
