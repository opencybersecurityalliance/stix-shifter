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
    from datadog_api_client.v2.model.incident_service_response_data import IncidentServiceResponseData
    from datadog_api_client.v2.model.incident_service_included_items import IncidentServiceIncludedItems
    from datadog_api_client.v2.model.user import User


class IncidentServiceResponse(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.incident_service_response_data import IncidentServiceResponseData
        from datadog_api_client.v2.model.incident_service_included_items import IncidentServiceIncludedItems

        return {
            "data": (IncidentServiceResponseData,),
            "included": ([IncidentServiceIncludedItems],),
        }

    attribute_map = {
        "data": "data",
        "included": "included",
    }
    read_only_vars = {
        "included",
    }

    def __init__(
        self_,
        data: IncidentServiceResponseData,
        included: Union[List[Union[IncidentServiceIncludedItems, User]], UnsetType] = unset,
        **kwargs,
    ):
        """
        Response with an incident service payload.

        :param data: Incident Service data from responses.
        :type data: IncidentServiceResponseData

        :param included: Included objects from relationships.
        :type included: [IncidentServiceIncludedItems], optional
        """
        if included is not unset:
            kwargs["included"] = included
        super().__init__(kwargs)

        self_.data = data
