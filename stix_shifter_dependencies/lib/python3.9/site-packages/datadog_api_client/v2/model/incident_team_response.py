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
    from datadog_api_client.v2.model.incident_team_response_data import IncidentTeamResponseData
    from datadog_api_client.v2.model.incident_team_included_items import IncidentTeamIncludedItems
    from datadog_api_client.v2.model.user import User


class IncidentTeamResponse(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.incident_team_response_data import IncidentTeamResponseData
        from datadog_api_client.v2.model.incident_team_included_items import IncidentTeamIncludedItems

        return {
            "data": (IncidentTeamResponseData,),
            "included": ([IncidentTeamIncludedItems],),
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
        data: IncidentTeamResponseData,
        included: Union[List[Union[IncidentTeamIncludedItems, User]], UnsetType] = unset,
        **kwargs,
    ):
        """
        Response with an incident team payload.

        :param data: Incident Team data from a response.
        :type data: IncidentTeamResponseData

        :param included: Included objects from relationships.
        :type included: [IncidentTeamIncludedItems], optional
        """
        if included is not unset:
            kwargs["included"] = included
        super().__init__(kwargs)

        self_.data = data
