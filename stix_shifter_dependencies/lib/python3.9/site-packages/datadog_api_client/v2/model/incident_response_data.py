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
    from datadog_api_client.v2.model.incident_response_attributes import IncidentResponseAttributes
    from datadog_api_client.v2.model.incident_response_relationships import IncidentResponseRelationships
    from datadog_api_client.v2.model.incident_type import IncidentType


class IncidentResponseData(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.incident_response_attributes import IncidentResponseAttributes
        from datadog_api_client.v2.model.incident_response_relationships import IncidentResponseRelationships
        from datadog_api_client.v2.model.incident_type import IncidentType

        return {
            "attributes": (IncidentResponseAttributes,),
            "id": (str,),
            "relationships": (IncidentResponseRelationships,),
            "type": (IncidentType,),
        }

    attribute_map = {
        "attributes": "attributes",
        "id": "id",
        "relationships": "relationships",
        "type": "type",
    }

    def __init__(
        self_,
        id: str,
        type: IncidentType,
        attributes: Union[IncidentResponseAttributes, UnsetType] = unset,
        relationships: Union[IncidentResponseRelationships, UnsetType] = unset,
        **kwargs,
    ):
        """
        Incident data from a response.

        :param attributes: The incident's attributes from a response.
        :type attributes: IncidentResponseAttributes, optional

        :param id: The incident's ID.
        :type id: str

        :param relationships: The incident's relationships from a response.
        :type relationships: IncidentResponseRelationships, optional

        :param type: Incident resource type.
        :type type: IncidentType
        """
        if attributes is not unset:
            kwargs["attributes"] = attributes
        if relationships is not unset:
            kwargs["relationships"] = relationships
        super().__init__(kwargs)

        self_.id = id
        self_.type = type
