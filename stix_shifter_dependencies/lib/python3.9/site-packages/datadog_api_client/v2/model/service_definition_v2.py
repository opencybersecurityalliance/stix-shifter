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
    from datadog_api_client.v2.model.service_definition_v2_contact import ServiceDefinitionV2Contact
    from datadog_api_client.v2.model.service_definition_v2_doc import ServiceDefinitionV2Doc
    from datadog_api_client.v2.model.service_definition_v2_integrations import ServiceDefinitionV2Integrations
    from datadog_api_client.v2.model.service_definition_v2_link import ServiceDefinitionV2Link
    from datadog_api_client.v2.model.service_definition_v2_repo import ServiceDefinitionV2Repo
    from datadog_api_client.v2.model.service_definition_v2_version import ServiceDefinitionV2Version
    from datadog_api_client.v2.model.service_definition_v2_email import ServiceDefinitionV2Email
    from datadog_api_client.v2.model.service_definition_v2_slack import ServiceDefinitionV2Slack
    from datadog_api_client.v2.model.service_definition_v2_ms_teams import ServiceDefinitionV2MSTeams


class ServiceDefinitionV2(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.service_definition_v2_contact import ServiceDefinitionV2Contact
        from datadog_api_client.v2.model.service_definition_v2_doc import ServiceDefinitionV2Doc
        from datadog_api_client.v2.model.service_definition_v2_integrations import ServiceDefinitionV2Integrations
        from datadog_api_client.v2.model.service_definition_v2_link import ServiceDefinitionV2Link
        from datadog_api_client.v2.model.service_definition_v2_repo import ServiceDefinitionV2Repo
        from datadog_api_client.v2.model.service_definition_v2_version import ServiceDefinitionV2Version

        return {
            "contacts": ([ServiceDefinitionV2Contact],),
            "dd_service": (str,),
            "dd_team": (str,),
            "docs": ([ServiceDefinitionV2Doc],),
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
            "integrations": (ServiceDefinitionV2Integrations,),
            "links": ([ServiceDefinitionV2Link],),
            "repos": ([ServiceDefinitionV2Repo],),
            "schema_version": (ServiceDefinitionV2Version,),
            "tags": ([str],),
            "team": (str,),
        }

    attribute_map = {
        "contacts": "contacts",
        "dd_service": "dd-service",
        "dd_team": "dd-team",
        "docs": "docs",
        "extensions": "extensions",
        "integrations": "integrations",
        "links": "links",
        "repos": "repos",
        "schema_version": "schema-version",
        "tags": "tags",
        "team": "team",
    }

    def __init__(
        self_,
        dd_service: str,
        schema_version: ServiceDefinitionV2Version,
        contacts: Union[
            List[
                Union[
                    ServiceDefinitionV2Contact,
                    ServiceDefinitionV2Email,
                    ServiceDefinitionV2Slack,
                    ServiceDefinitionV2MSTeams,
                ]
            ],
            UnsetType,
        ] = unset,
        dd_team: Union[str, UnsetType] = unset,
        docs: Union[List[ServiceDefinitionV2Doc], UnsetType] = unset,
        extensions: Union[Dict[str, Any], UnsetType] = unset,
        integrations: Union[ServiceDefinitionV2Integrations, UnsetType] = unset,
        links: Union[List[ServiceDefinitionV2Link], UnsetType] = unset,
        repos: Union[List[ServiceDefinitionV2Repo], UnsetType] = unset,
        tags: Union[List[str], UnsetType] = unset,
        team: Union[str, UnsetType] = unset,
        **kwargs,
    ):
        """
        Service definition V2 for providing service metadata and integrations.

        :param contacts: A list of contacts related to the services.
        :type contacts: [ServiceDefinitionV2Contact], optional

        :param dd_service: Unique identifier of the service. Must be unique across all services and is used to match with a service in Datadog.
        :type dd_service: str

        :param dd_team: Experimental feature. A Team handle that matches a Team in the Datadog Teams product.
        :type dd_team: str, optional

        :param docs: A list of documentation related to the services.
        :type docs: [ServiceDefinitionV2Doc], optional

        :param extensions: Extensions to V2 schema.
        :type extensions: {str: (bool, date, datetime, dict, float, int, list, str, none_type,)}, optional

        :param integrations: Third party integrations that Datadog supports.
        :type integrations: ServiceDefinitionV2Integrations, optional

        :param links: A list of links related to the services.
        :type links: [ServiceDefinitionV2Link], optional

        :param repos: A list of code repositories related to the services.
        :type repos: [ServiceDefinitionV2Repo], optional

        :param schema_version: Schema version being used.
        :type schema_version: ServiceDefinitionV2Version

        :param tags: A set of custom tags.
        :type tags: [str], optional

        :param team: Team that owns the service.
        :type team: str, optional
        """
        if contacts is not unset:
            kwargs["contacts"] = contacts
        if dd_team is not unset:
            kwargs["dd_team"] = dd_team
        if docs is not unset:
            kwargs["docs"] = docs
        if extensions is not unset:
            kwargs["extensions"] = extensions
        if integrations is not unset:
            kwargs["integrations"] = integrations
        if links is not unset:
            kwargs["links"] = links
        if repos is not unset:
            kwargs["repos"] = repos
        if tags is not unset:
            kwargs["tags"] = tags
        if team is not unset:
            kwargs["team"] = team
        super().__init__(kwargs)

        self_.dd_service = dd_service
        self_.schema_version = schema_version
