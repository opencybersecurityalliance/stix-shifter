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
    from datadog_api_client.v2.model.incident_integration_metadata_attributes import (
        IncidentIntegrationMetadataAttributes,
    )
    from datadog_api_client.v2.model.incident_integration_metadata_type import IncidentIntegrationMetadataType


class IncidentIntegrationMetadataCreateData(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.incident_integration_metadata_attributes import (
            IncidentIntegrationMetadataAttributes,
        )
        from datadog_api_client.v2.model.incident_integration_metadata_type import IncidentIntegrationMetadataType

        return {
            "attributes": (IncidentIntegrationMetadataAttributes,),
            "type": (IncidentIntegrationMetadataType,),
        }

    attribute_map = {
        "attributes": "attributes",
        "type": "type",
    }

    def __init__(
        self_, attributes: IncidentIntegrationMetadataAttributes, type: IncidentIntegrationMetadataType, **kwargs
    ):
        """
        Incident integration metadata data for a create request.

        :param attributes: Incident integration metadata's attributes for a create request.
        :type attributes: IncidentIntegrationMetadataAttributes

        :param type: Integration metadata resource type.
        :type type: IncidentIntegrationMetadataType
        """
        super().__init__(kwargs)

        self_.attributes = attributes
        self_.type = type
