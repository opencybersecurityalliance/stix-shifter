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
    from datadog_api_client.v2.model.incident_integration_metadata_metadata import IncidentIntegrationMetadataMetadata
    from datadog_api_client.v2.model.slack_integration_metadata import SlackIntegrationMetadata
    from datadog_api_client.v2.model.jira_integration_metadata import JiraIntegrationMetadata


class IncidentIntegrationMetadataAttributes(ModelNormal):
    validations = {
        "integration_type": {
            "inclusive_maximum": 9,
        },
        "status": {
            "inclusive_maximum": 5,
        },
    }

    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.incident_integration_metadata_metadata import (
            IncidentIntegrationMetadataMetadata,
        )

        return {
            "incident_id": (str,),
            "integration_type": (int,),
            "metadata": (IncidentIntegrationMetadataMetadata,),
            "status": (int,),
        }

    attribute_map = {
        "incident_id": "incident_id",
        "integration_type": "integration_type",
        "metadata": "metadata",
        "status": "status",
    }

    def __init__(
        self_,
        integration_type: int,
        metadata: Union[IncidentIntegrationMetadataMetadata, SlackIntegrationMetadata, JiraIntegrationMetadata],
        incident_id: Union[str, UnsetType] = unset,
        status: Union[int, UnsetType] = unset,
        **kwargs,
    ):
        """
        Incident integration metadata's attributes for a create request.

        :param incident_id: UUID of the incident this integration metadata is connected to.
        :type incident_id: str, optional

        :param integration_type: A number indicating the type of integration this metadata is for. 1 indicates Slack;
            8 indicates Jira.
        :type integration_type: int

        :param metadata: Incident integration metadata's metadata attribute.
        :type metadata: IncidentIntegrationMetadataMetadata

        :param status: A number indicating the status of this integration metadata. 0 indicates unknown;
            1 indicates pending; 2 indicates complete; 3 indicates manually created;
            4 indicates manually updated; 5 indicates failed.
        :type status: int, optional
        """
        if incident_id is not unset:
            kwargs["incident_id"] = incident_id
        if status is not unset:
            kwargs["status"] = status
        super().__init__(kwargs)

        self_.integration_type = integration_type
        self_.metadata = metadata
