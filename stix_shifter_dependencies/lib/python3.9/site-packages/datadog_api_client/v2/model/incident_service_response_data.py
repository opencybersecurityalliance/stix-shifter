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
    from datadog_api_client.v2.model.incident_service_response_attributes import IncidentServiceResponseAttributes
    from datadog_api_client.v2.model.incident_service_relationships import IncidentServiceRelationships
    from datadog_api_client.v2.model.incident_service_type import IncidentServiceType


class IncidentServiceResponseData(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.incident_service_response_attributes import IncidentServiceResponseAttributes
        from datadog_api_client.v2.model.incident_service_relationships import IncidentServiceRelationships
        from datadog_api_client.v2.model.incident_service_type import IncidentServiceType

        return {
            "attributes": (IncidentServiceResponseAttributes,),
            "id": (str,),
            "relationships": (IncidentServiceRelationships,),
            "type": (IncidentServiceType,),
        }

    attribute_map = {
        "attributes": "attributes",
        "id": "id",
        "relationships": "relationships",
        "type": "type",
    }
    read_only_vars = {
        "relationships",
    }

    def __init__(
        self_,
        id: str,
        type: IncidentServiceType,
        attributes: Union[IncidentServiceResponseAttributes, UnsetType] = unset,
        relationships: Union[IncidentServiceRelationships, UnsetType] = unset,
        **kwargs,
    ):
        """
        Incident Service data from responses.

        :param attributes: The incident service's attributes from a response.
        :type attributes: IncidentServiceResponseAttributes, optional

        :param id: The incident service's ID.
        :type id: str

        :param relationships: The incident service's relationships.
        :type relationships: IncidentServiceRelationships, optional

        :param type: Incident service resource type.
        :type type: IncidentServiceType
        """
        if attributes is not unset:
            kwargs["attributes"] = attributes
        if relationships is not unset:
            kwargs["relationships"] = relationships
        super().__init__(kwargs)

        self_.id = id
        self_.type = type
