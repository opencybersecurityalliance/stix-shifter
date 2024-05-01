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
    from datadog_api_client.v2.model.incident_integration_metadata_response_data import (
        IncidentIntegrationMetadataResponseData,
    )
    from datadog_api_client.v2.model.incident_integration_metadata_response_included_item import (
        IncidentIntegrationMetadataResponseIncludedItem,
    )
    from datadog_api_client.v2.model.user import User


class IncidentIntegrationMetadataResponse(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.incident_integration_metadata_response_data import (
            IncidentIntegrationMetadataResponseData,
        )
        from datadog_api_client.v2.model.incident_integration_metadata_response_included_item import (
            IncidentIntegrationMetadataResponseIncludedItem,
        )

        return {
            "data": (IncidentIntegrationMetadataResponseData,),
            "included": ([IncidentIntegrationMetadataResponseIncludedItem],),
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
        data: IncidentIntegrationMetadataResponseData,
        included: Union[List[Union[IncidentIntegrationMetadataResponseIncludedItem, User]], UnsetType] = unset,
        **kwargs,
    ):
        """
        Response with an incident integration metadata.

        :param data: Incident integration metadata from a response.
        :type data: IncidentIntegrationMetadataResponseData

        :param included: Included related resources that the user requested.
        :type included: [IncidentIntegrationMetadataResponseIncludedItem], optional
        """
        if included is not unset:
            kwargs["included"] = included
        super().__init__(kwargs)

        self_.data = data
