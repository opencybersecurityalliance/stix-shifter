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
    from datadog_api_client.v2.model.incident_search_response_user_facet_data import IncidentSearchResponseUserFacetData
    from datadog_api_client.v2.model.incident_search_response_property_field_facet_data import (
        IncidentSearchResponsePropertyFieldFacetData,
    )
    from datadog_api_client.v2.model.incident_search_response_field_facet_data import (
        IncidentSearchResponseFieldFacetData,
    )
    from datadog_api_client.v2.model.incident_search_response_numeric_facet_data import (
        IncidentSearchResponseNumericFacetData,
    )


class IncidentSearchResponseFacetsData(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.incident_search_response_user_facet_data import (
            IncidentSearchResponseUserFacetData,
        )
        from datadog_api_client.v2.model.incident_search_response_property_field_facet_data import (
            IncidentSearchResponsePropertyFieldFacetData,
        )
        from datadog_api_client.v2.model.incident_search_response_field_facet_data import (
            IncidentSearchResponseFieldFacetData,
        )
        from datadog_api_client.v2.model.incident_search_response_numeric_facet_data import (
            IncidentSearchResponseNumericFacetData,
        )

        return {
            "commander": ([IncidentSearchResponseUserFacetData],),
            "created_by": ([IncidentSearchResponseUserFacetData],),
            "fields": ([IncidentSearchResponsePropertyFieldFacetData],),
            "impact": ([IncidentSearchResponseFieldFacetData],),
            "last_modified_by": ([IncidentSearchResponseUserFacetData],),
            "postmortem": ([IncidentSearchResponseFieldFacetData],),
            "responder": ([IncidentSearchResponseUserFacetData],),
            "severity": ([IncidentSearchResponseFieldFacetData],),
            "state": ([IncidentSearchResponseFieldFacetData],),
            "time_to_repair": ([IncidentSearchResponseNumericFacetData],),
            "time_to_resolve": ([IncidentSearchResponseNumericFacetData],),
        }

    attribute_map = {
        "commander": "commander",
        "created_by": "created_by",
        "fields": "fields",
        "impact": "impact",
        "last_modified_by": "last_modified_by",
        "postmortem": "postmortem",
        "responder": "responder",
        "severity": "severity",
        "state": "state",
        "time_to_repair": "time_to_repair",
        "time_to_resolve": "time_to_resolve",
    }

    def __init__(
        self_,
        commander: Union[List[IncidentSearchResponseUserFacetData], UnsetType] = unset,
        created_by: Union[List[IncidentSearchResponseUserFacetData], UnsetType] = unset,
        fields: Union[List[IncidentSearchResponsePropertyFieldFacetData], UnsetType] = unset,
        impact: Union[List[IncidentSearchResponseFieldFacetData], UnsetType] = unset,
        last_modified_by: Union[List[IncidentSearchResponseUserFacetData], UnsetType] = unset,
        postmortem: Union[List[IncidentSearchResponseFieldFacetData], UnsetType] = unset,
        responder: Union[List[IncidentSearchResponseUserFacetData], UnsetType] = unset,
        severity: Union[List[IncidentSearchResponseFieldFacetData], UnsetType] = unset,
        state: Union[List[IncidentSearchResponseFieldFacetData], UnsetType] = unset,
        time_to_repair: Union[List[IncidentSearchResponseNumericFacetData], UnsetType] = unset,
        time_to_resolve: Union[List[IncidentSearchResponseNumericFacetData], UnsetType] = unset,
        **kwargs,
    ):
        """
        Facet data for incidents returned by a search query.

        :param commander: Facet data for incident commander users.
        :type commander: [IncidentSearchResponseUserFacetData], optional

        :param created_by: Facet data for incident creator users.
        :type created_by: [IncidentSearchResponseUserFacetData], optional

        :param fields: Facet data for incident property fields.
        :type fields: [IncidentSearchResponsePropertyFieldFacetData], optional

        :param impact: Facet data for incident impact attributes.
        :type impact: [IncidentSearchResponseFieldFacetData], optional

        :param last_modified_by: Facet data for incident last modified by users.
        :type last_modified_by: [IncidentSearchResponseUserFacetData], optional

        :param postmortem: Facet data for incident postmortem existence.
        :type postmortem: [IncidentSearchResponseFieldFacetData], optional

        :param responder: Facet data for incident responder users.
        :type responder: [IncidentSearchResponseUserFacetData], optional

        :param severity: Facet data for incident severity attributes.
        :type severity: [IncidentSearchResponseFieldFacetData], optional

        :param state: Facet data for incident state attributes.
        :type state: [IncidentSearchResponseFieldFacetData], optional

        :param time_to_repair: Facet data for incident time to repair metrics.
        :type time_to_repair: [IncidentSearchResponseNumericFacetData], optional

        :param time_to_resolve: Facet data for incident time to resolve metrics.
        :type time_to_resolve: [IncidentSearchResponseNumericFacetData], optional
        """
        if commander is not unset:
            kwargs["commander"] = commander
        if created_by is not unset:
            kwargs["created_by"] = created_by
        if fields is not unset:
            kwargs["fields"] = fields
        if impact is not unset:
            kwargs["impact"] = impact
        if last_modified_by is not unset:
            kwargs["last_modified_by"] = last_modified_by
        if postmortem is not unset:
            kwargs["postmortem"] = postmortem
        if responder is not unset:
            kwargs["responder"] = responder
        if severity is not unset:
            kwargs["severity"] = severity
        if state is not unset:
            kwargs["state"] = state
        if time_to_repair is not unset:
            kwargs["time_to_repair"] = time_to_repair
        if time_to_resolve is not unset:
            kwargs["time_to_resolve"] = time_to_resolve
        super().__init__(kwargs)
