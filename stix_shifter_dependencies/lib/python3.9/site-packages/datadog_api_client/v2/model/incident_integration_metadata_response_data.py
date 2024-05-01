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
    from datadog_api_client.v2.model.incident_integration_metadata_attributes import (
        IncidentIntegrationMetadataAttributes,
    )
    from datadog_api_client.v2.model.incident_integration_metadata_type import IncidentIntegrationMetadataType


class IncidentIntegrationMetadataResponseData(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.incident_integration_metadata_attributes import (
            IncidentIntegrationMetadataAttributes,
        )
        from datadog_api_client.v2.model.incident_integration_metadata_type import IncidentIntegrationMetadataType

        return {
            "attributes": (IncidentIntegrationMetadataAttributes,),
            "id": (str,),
            "type": (IncidentIntegrationMetadataType,),
        }

    attribute_map = {
        "attributes": "attributes",
        "id": "id",
        "type": "type",
    }

    def __init__(
        self_,
        id: str,
        type: IncidentIntegrationMetadataType,
        attributes: Union[IncidentIntegrationMetadataAttributes, UnsetType] = unset,
        **kwargs,
    ):
        """
        Incident integration metadata from a response.

        :param attributes: Incident integration metadata's attributes for a create request.
        :type attributes: IncidentIntegrationMetadataAttributes, optional

        :param id: The incident integration metadata's ID.
        :type id: str

        :param type: Integration metadata resource type.
        :type type: IncidentIntegrationMetadataType
        """
        if attributes is not unset:
            kwargs["attributes"] = attributes
        super().__init__(kwargs)

        self_.id = id
        self_.type = type
