# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import TYPE_CHECKING

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
)


if TYPE_CHECKING:
    from datadog_api_client.v2.model.incident_search_response_numeric_facet_data_aggregates import (
        IncidentSearchResponseNumericFacetDataAggregates,
    )


class IncidentSearchResponseNumericFacetData(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.incident_search_response_numeric_facet_data_aggregates import (
            IncidentSearchResponseNumericFacetDataAggregates,
        )

        return {
            "aggregates": (IncidentSearchResponseNumericFacetDataAggregates,),
            "name": (str,),
        }

    attribute_map = {
        "aggregates": "aggregates",
        "name": "name",
    }

    def __init__(self_, aggregates: IncidentSearchResponseNumericFacetDataAggregates, name: str, **kwargs):
        """
        Facet data numeric attributes of an incident.

        :param aggregates: Aggregate information for numeric incident data.
        :type aggregates: IncidentSearchResponseNumericFacetDataAggregates

        :param name: Name of the incident property field.
        :type name: str
        """
        super().__init__(kwargs)

        self_.aggregates = aggregates
        self_.name = name
