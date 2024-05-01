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
    from datadog_api_client.v2.model.incident_search_response_attributes import IncidentSearchResponseAttributes
    from datadog_api_client.v2.model.incident_search_results_type import IncidentSearchResultsType


class IncidentSearchResponseData(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.incident_search_response_attributes import IncidentSearchResponseAttributes
        from datadog_api_client.v2.model.incident_search_results_type import IncidentSearchResultsType

        return {
            "attributes": (IncidentSearchResponseAttributes,),
            "type": (IncidentSearchResultsType,),
        }

    attribute_map = {
        "attributes": "attributes",
        "type": "type",
    }

    def __init__(
        self_,
        attributes: Union[IncidentSearchResponseAttributes, UnsetType] = unset,
        type: Union[IncidentSearchResultsType, UnsetType] = unset,
        **kwargs,
    ):
        """
        Data returned by an incident search.

        :param attributes: Attributes returned by an incident search.
        :type attributes: IncidentSearchResponseAttributes, optional

        :param type: Incident search result type.
        :type type: IncidentSearchResultsType, optional
        """
        if attributes is not unset:
            kwargs["attributes"] = attributes
        if type is not unset:
            kwargs["type"] = type
        super().__init__(kwargs)
