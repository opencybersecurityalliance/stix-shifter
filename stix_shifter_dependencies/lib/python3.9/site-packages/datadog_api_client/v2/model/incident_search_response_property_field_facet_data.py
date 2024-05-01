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
    from datadog_api_client.v2.model.incident_search_response_numeric_facet_data_aggregates import (
        IncidentSearchResponseNumericFacetDataAggregates,
    )
    from datadog_api_client.v2.model.incident_search_response_field_facet_data import (
        IncidentSearchResponseFieldFacetData,
    )


class IncidentSearchResponsePropertyFieldFacetData(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.incident_search_response_numeric_facet_data_aggregates import (
            IncidentSearchResponseNumericFacetDataAggregates,
        )
        from datadog_api_client.v2.model.incident_search_response_field_facet_data import (
            IncidentSearchResponseFieldFacetData,
        )

        return {
            "aggregates": (IncidentSearchResponseNumericFacetDataAggregates,),
            "facets": ([IncidentSearchResponseFieldFacetData],),
            "name": (str,),
        }

    attribute_map = {
        "aggregates": "aggregates",
        "facets": "facets",
        "name": "name",
    }

    def __init__(
        self_,
        facets: List[IncidentSearchResponseFieldFacetData],
        name: str,
        aggregates: Union[IncidentSearchResponseNumericFacetDataAggregates, UnsetType] = unset,
        **kwargs,
    ):
        """
        Facet data for the incident property fields.

        :param aggregates: Aggregate information for numeric incident data.
        :type aggregates: IncidentSearchResponseNumericFacetDataAggregates, optional

        :param facets: Facet data for the property field of an incident.
        :type facets: [IncidentSearchResponseFieldFacetData]

        :param name: Name of the incident property field.
        :type name: str
        """
        if aggregates is not unset:
            kwargs["aggregates"] = aggregates
        super().__init__(kwargs)

        self_.facets = facets
        self_.name = name
