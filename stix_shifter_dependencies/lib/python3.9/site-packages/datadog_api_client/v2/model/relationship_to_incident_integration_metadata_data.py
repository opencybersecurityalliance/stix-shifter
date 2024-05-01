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
    from datadog_api_client.v2.model.incident_integration_metadata_type import IncidentIntegrationMetadataType


class RelationshipToIncidentIntegrationMetadataData(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.incident_integration_metadata_type import IncidentIntegrationMetadataType

        return {
            "id": (str,),
            "type": (IncidentIntegrationMetadataType,),
        }

    attribute_map = {
        "id": "id",
        "type": "type",
    }

    def __init__(self_, id: str, type: IncidentIntegrationMetadataType, **kwargs):
        """
        A relationship reference for an integration metadata object.

        :param id: A unique identifier that represents the integration metadata.
        :type id: str

        :param type: Integration metadata resource type.
        :type type: IncidentIntegrationMetadataType
        """
        super().__init__(kwargs)

        self_.id = id
        self_.type = type
