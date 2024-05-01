# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Any, Dict, List, Union, TYPE_CHECKING

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    date,
    datetime,
    none_type,
    unset,
    UnsetType,
)


if TYPE_CHECKING:
    from datadog_api_client.v2.model.service_definition_v2_dot1_contact import ServiceDefinitionV2Dot1Contact
    from datadog_api_client.v2.model.service_definition_v2_dot1_integrations import ServiceDefinitionV2Dot1Integrations
    from datadog_api_client.v2.model.service_definition_v2_dot1_link import ServiceDefinitionV2Dot1Link
    from datadog_api_client.v2.model.service_definition_v2_dot1_version import ServiceDefinitionV2Dot1Version
    from datadog_api_client.v2.model.service_definition_v2_dot1_email import ServiceDefinitionV2Dot1Email
    from datadog_api_client.v2.model.service_definition_v2_dot1_slack import ServiceDefinitionV2Dot1Slack
    from datadog_api_client.v2.model.service_definition_v2_dot1_ms_teams import ServiceDefinitionV2Dot1MSTeams


class ServiceDefinitionV2Dot1(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.service_definition_v2_dot1_contact import ServiceDefinitionV2Dot1Contact
        from datadog_api_client.v2.model.service_definition_v2_dot1_integrations import (
            ServiceDefinitionV2Dot1Integrations,
        )
        from datadog_api_client.v2.model.service_definition_v2_dot1_link import ServiceDefinitionV2Dot1Link
        from datadog_api_client.v2.model.service_definition_v2_dot1_version import ServiceDefinitionV2Dot1Version

        return {
            "application": (str,),
            "contacts": ([ServiceDefinitionV2Dot1Contact],),
            "dd_service": (str,),
            "description": (str,),
            "extensions": (
                {
                    str: (
                        bool,
                        date,
                        datetime,
                        dict,
                        float,
                        int,
                        list,
                        str,
                        none_type,
                    )
                },
            ),
            "integrations": (ServiceDefinitionV2Dot1Integrations,),
            "lifecycle": (str,),
            "links": ([ServiceDefinitionV2Dot1Link],),
            "schema_version": (ServiceDefinitionV2Dot1Version,),
            "tags": ([str],),
            "team": (str,),
            "tier": (str,),
        }

    attribute_map = {
        "application": "application",
        "contacts": "contacts",
        "dd_service": "dd-service",
        "description": "description",
        "extensions": "extensions",
        "integrations": "integrations",
        "lifecycle": "lifecycle",
        "links": "links",
        "schema_version": "schema-version",
        "tags": "tags",
        "team": "team",
        "tier": "tier",
    }

    def __init__(
        self_,
        dd_service: str,
        schema_version: ServiceDefinitionV2Dot1Version,
        application: Union[str, UnsetType] = unset,
        contacts: Union[
            List[
                Union[
                    ServiceDefinitionV2Dot1Contact,
                    ServiceDefinitionV2Dot1Email,
                    ServiceDefinitionV2Dot1Slack,
                    ServiceDefinitionV2Dot1MSTeams,
                ]
            ],
            UnsetType,
        ] = unset,
        description: Union[str, UnsetType] = unset,
        extensions: Union[Dict[str, Any], UnsetType] = unset,
        integrations: Union[ServiceDefinitionV2Dot1Integrations, UnsetType] = unset,
        lifecycle: Union[str, UnsetType] = unset,
        links: Union[List[ServiceDefinitionV2Dot1Link], UnsetType] = unset,
        tags: Union[List[str], UnsetType] = unset,
        team: Union[str, UnsetType] = unset,
        tier: Union[str, UnsetType] = unset,
        **kwargs,
    ):
        """
        Service definition v2.1 for providing service metadata and integrations.

        :param application: Identifier for a group of related services serving a product feature, which the service is a part of.
        :type application: str, optional

        :param contacts: A list of contacts related to the services.
        :type contacts: [ServiceDefinitionV2Dot1Contact], optional

        :param dd_service: Unique identifier of the service. Must be unique across all services and is used to match with a service in Datadog.
        :type dd_service: str

        :param description: A short description of the service.
        :type description: str, optional

        :param extensions: Extensions to v2.1 schema.
        :type extensions: {str: (bool, date, datetime, dict, float, int, list, str, none_type,)}, optional

        :param integrations: Third party integrations that Datadog supports.
        :type integrations: ServiceDefinitionV2Dot1Integrations, optional

        :param lifecycle: The current life cycle phase of the service.
        :type lifecycle: str, optional

        :param links: A list of links related to the services.
        :type links: [ServiceDefinitionV2Dot1Link], optional

        :param schema_version: Schema version being used.
        :type schema_version: ServiceDefinitionV2Dot1Version

        :param tags: A set of custom tags.
        :type tags: [str], optional

        :param team: Team that owns the service. It is used to locate a team defined in Datadog Teams if it exists.
        :type team: str, optional

        :param tier: Importance of the service.
        :type tier: str, optional
        """
        if application is not unset:
            kwargs["application"] = application
        if contacts is not unset:
            kwargs["contacts"] = contacts
        if description is not unset:
            kwargs["description"] = description
        if extensions is not unset:
            kwargs["extensions"] = extensions
        if integrations is not unset:
            kwargs["integrations"] = integrations
        if lifecycle is not unset:
            kwargs["lifecycle"] = lifecycle
        if links is not unset:
            kwargs["links"] = links
        if tags is not unset:
            kwargs["tags"] = tags
        if team is not unset:
            kwargs["team"] = team
        if tier is not unset:
            kwargs["tier"] = tier
        super().__init__(kwargs)

        self_.dd_service = dd_service
        self_.schema_version = schema_version
