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
    from datadog_api_client.v2.model.incident_response_meta import IncidentResponseMeta
    from datadog_api_client.v2.model.user import User


class IncidentIntegrationMetadataListResponse(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.incident_integration_metadata_response_data import (
            IncidentIntegrationMetadataResponseData,
        )
        from datadog_api_client.v2.model.incident_integration_metadata_response_included_item import (
            IncidentIntegrationMetadataResponseIncludedItem,
        )
        from datadog_api_client.v2.model.incident_response_meta import IncidentResponseMeta

        return {
            "data": ([IncidentIntegrationMetadataResponseData],),
            "included": ([IncidentIntegrationMetadataResponseIncludedItem],),
            "meta": (IncidentResponseMeta,),
        }

    attribute_map = {
        "data": "data",
        "included": "included",
        "meta": "meta",
    }
    read_only_vars = {
        "included",
        "meta",
    }

    def __init__(
        self_,
        data: List[IncidentIntegrationMetadataResponseData],
        included: Union[List[Union[IncidentIntegrationMetadataResponseIncludedItem, User]], UnsetType] = unset,
        meta: Union[IncidentResponseMeta, UnsetType] = unset,
        **kwargs,
    ):
        """
        Response with a list of incident integration metadata.

        :param data: An array of incident integration metadata.
        :type data: [IncidentIntegrationMetadataResponseData]

        :param included: Included related resources that the user requested.
        :type included: [IncidentIntegrationMetadataResponseIncludedItem], optional

        :param meta: The metadata object containing pagination metadata.
        :type meta: IncidentResponseMeta, optional
        """
        if included is not unset:
            kwargs["included"] = included
        if meta is not unset:
            kwargs["meta"] = meta
        super().__init__(kwargs)

        self_.data = data
