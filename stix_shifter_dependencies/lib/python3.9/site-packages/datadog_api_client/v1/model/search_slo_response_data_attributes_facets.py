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
    from datadog_api_client.v1.model.search_slo_response_data_attributes_facets_object_string import (
        SearchSLOResponseDataAttributesFacetsObjectString,
    )
    from datadog_api_client.v1.model.search_slo_response_data_attributes_facets_object_int import (
        SearchSLOResponseDataAttributesFacetsObjectInt,
    )


class SearchSLOResponseDataAttributesFacets(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.search_slo_response_data_attributes_facets_object_string import (
            SearchSLOResponseDataAttributesFacetsObjectString,
        )
        from datadog_api_client.v1.model.search_slo_response_data_attributes_facets_object_int import (
            SearchSLOResponseDataAttributesFacetsObjectInt,
        )

        return {
            "all_tags": ([SearchSLOResponseDataAttributesFacetsObjectString],),
            "creator_name": ([SearchSLOResponseDataAttributesFacetsObjectString],),
            "env_tags": ([SearchSLOResponseDataAttributesFacetsObjectString],),
            "service_tags": ([SearchSLOResponseDataAttributesFacetsObjectString],),
            "slo_type": ([SearchSLOResponseDataAttributesFacetsObjectInt],),
            "target": ([SearchSLOResponseDataAttributesFacetsObjectInt],),
            "team_tags": ([SearchSLOResponseDataAttributesFacetsObjectString],),
            "timeframe": ([SearchSLOResponseDataAttributesFacetsObjectString],),
        }

    attribute_map = {
        "all_tags": "all_tags",
        "creator_name": "creator_name",
        "env_tags": "env_tags",
        "service_tags": "service_tags",
        "slo_type": "slo_type",
        "target": "target",
        "team_tags": "team_tags",
        "timeframe": "timeframe",
    }

    def __init__(
        self_,
        all_tags: Union[List[SearchSLOResponseDataAttributesFacetsObjectString], UnsetType] = unset,
        creator_name: Union[List[SearchSLOResponseDataAttributesFacetsObjectString], UnsetType] = unset,
        env_tags: Union[List[SearchSLOResponseDataAttributesFacetsObjectString], UnsetType] = unset,
        service_tags: Union[List[SearchSLOResponseDataAttributesFacetsObjectString], UnsetType] = unset,
        slo_type: Union[List[SearchSLOResponseDataAttributesFacetsObjectInt], UnsetType] = unset,
        target: Union[List[SearchSLOResponseDataAttributesFacetsObjectInt], UnsetType] = unset,
        team_tags: Union[List[SearchSLOResponseDataAttributesFacetsObjectString], UnsetType] = unset,
        timeframe: Union[List[SearchSLOResponseDataAttributesFacetsObjectString], UnsetType] = unset,
        **kwargs,
    ):
        """
        Facets

        :param all_tags: All tags associated with an SLO.
        :type all_tags: [SearchSLOResponseDataAttributesFacetsObjectString], optional

        :param creator_name: Creator of an SLO.
        :type creator_name: [SearchSLOResponseDataAttributesFacetsObjectString], optional

        :param env_tags: Tags with the ``env`` tag key.
        :type env_tags: [SearchSLOResponseDataAttributesFacetsObjectString], optional

        :param service_tags: Tags with the ``service`` tag key.
        :type service_tags: [SearchSLOResponseDataAttributesFacetsObjectString], optional

        :param slo_type: Type of SLO.
        :type slo_type: [SearchSLOResponseDataAttributesFacetsObjectInt], optional

        :param target: SLO Target
        :type target: [SearchSLOResponseDataAttributesFacetsObjectInt], optional

        :param team_tags: Tags with the ``team`` tag key.
        :type team_tags: [SearchSLOResponseDataAttributesFacetsObjectString], optional

        :param timeframe: Timeframes of SLOs.
        :type timeframe: [SearchSLOResponseDataAttributesFacetsObjectString], optional
        """
        if all_tags is not unset:
            kwargs["all_tags"] = all_tags
        if creator_name is not unset:
            kwargs["creator_name"] = creator_name
        if env_tags is not unset:
            kwargs["env_tags"] = env_tags
        if service_tags is not unset:
            kwargs["service_tags"] = service_tags
        if slo_type is not unset:
            kwargs["slo_type"] = slo_type
        if target is not unset:
            kwargs["target"] = target
        if team_tags is not unset:
            kwargs["team_tags"] = team_tags
        if timeframe is not unset:
            kwargs["timeframe"] = timeframe
        super().__init__(kwargs)
