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
    from datadog_api_client.v2.model.incident_search_response_facets_data import IncidentSearchResponseFacetsData
    from datadog_api_client.v2.model.incident_search_response_incidents_data import IncidentSearchResponseIncidentsData


class IncidentSearchResponseAttributes(ModelNormal):
    validations = {
        "total": {
            "inclusive_maximum": 2147483647,
        },
    }

    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.incident_search_response_facets_data import IncidentSearchResponseFacetsData
        from datadog_api_client.v2.model.incident_search_response_incidents_data import (
            IncidentSearchResponseIncidentsData,
        )

        return {
            "facets": (IncidentSearchResponseFacetsData,),
            "incidents": ([IncidentSearchResponseIncidentsData],),
            "total": (int,),
        }

    attribute_map = {
        "facets": "facets",
        "incidents": "incidents",
        "total": "total",
    }

    def __init__(
        self_,
        facets: IncidentSearchResponseFacetsData,
        incidents: List[IncidentSearchResponseIncidentsData],
        total: int,
        **kwargs,
    ):
        """
        Attributes returned by an incident search.

        :param facets: Facet data for incidents returned by a search query.
        :type facets: IncidentSearchResponseFacetsData

        :param incidents: Incidents returned by the search.
        :type incidents: [IncidentSearchResponseIncidentsData]

        :param total: Number of incidents returned by the search.
        :type total: int
        """
        super().__init__(kwargs)

        self_.facets = facets
        self_.incidents = incidents
        self_.total = total
