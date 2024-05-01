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
    from datadog_api_client.v2.model.service_definition_v1_contact import ServiceDefinitionV1Contact
    from datadog_api_client.v2.model.service_definition_v1_resource import ServiceDefinitionV1Resource
    from datadog_api_client.v2.model.service_definition_v1_info import ServiceDefinitionV1Info
    from datadog_api_client.v2.model.service_definition_v1_integrations import ServiceDefinitionV1Integrations
    from datadog_api_client.v2.model.service_definition_v1_org import ServiceDefinitionV1Org
    from datadog_api_client.v2.model.service_definition_v1_version import ServiceDefinitionV1Version


class ServiceDefinitionV1(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.service_definition_v1_contact import ServiceDefinitionV1Contact
        from datadog_api_client.v2.model.service_definition_v1_resource import ServiceDefinitionV1Resource
        from datadog_api_client.v2.model.service_definition_v1_info import ServiceDefinitionV1Info
        from datadog_api_client.v2.model.service_definition_v1_integrations import ServiceDefinitionV1Integrations
        from datadog_api_client.v2.model.service_definition_v1_org import ServiceDefinitionV1Org
        from datadog_api_client.v2.model.service_definition_v1_version import ServiceDefinitionV1Version

        return {
            "contact": (ServiceDefinitionV1Contact,),
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
            "external_resources": ([ServiceDefinitionV1Resource],),
            "info": (ServiceDefinitionV1Info,),
            "integrations": (ServiceDefinitionV1Integrations,),
            "org": (ServiceDefinitionV1Org,),
            "schema_version": (ServiceDefinitionV1Version,),
            "tags": ([str],),
        }

    attribute_map = {
        "contact": "contact",
        "extensions": "extensions",
        "external_resources": "external-resources",
        "info": "info",
        "integrations": "integrations",
        "org": "org",
        "schema_version": "schema-version",
        "tags": "tags",
    }

    def __init__(
        self_,
        info: ServiceDefinitionV1Info,
        schema_version: ServiceDefinitionV1Version,
        contact: Union[ServiceDefinitionV1Contact, UnsetType] = unset,
        extensions: Union[Dict[str, Any], UnsetType] = unset,
        external_resources: Union[List[ServiceDefinitionV1Resource], UnsetType] = unset,
        integrations: Union[ServiceDefinitionV1Integrations, UnsetType] = unset,
        org: Union[ServiceDefinitionV1Org, UnsetType] = unset,
        tags: Union[List[str], UnsetType] = unset,
        **kwargs,
    ):
        """
        Deprecated - Service definition V1 for providing additional service metadata and integrations.

        :param contact: Contact information about the service.
        :type contact: ServiceDefinitionV1Contact, optional

        :param extensions: Extensions to V1 schema.
        :type extensions: {str: (bool, date, datetime, dict, float, int, list, str, none_type,)}, optional

        :param external_resources: A list of external links related to the services.
        :type external_resources: [ServiceDefinitionV1Resource], optional

        :param info: Basic information about a service.
        :type info: ServiceDefinitionV1Info

        :param integrations: Third party integrations that Datadog supports.
        :type integrations: ServiceDefinitionV1Integrations, optional

        :param org: Org related information about the service.
        :type org: ServiceDefinitionV1Org, optional

        :param schema_version: Schema version being used.
        :type schema_version: ServiceDefinitionV1Version

        :param tags: A set of custom tags.
        :type tags: [str], optional
        """
        if contact is not unset:
            kwargs["contact"] = contact
        if extensions is not unset:
            kwargs["extensions"] = extensions
        if external_resources is not unset:
            kwargs["external_resources"] = external_resources
        if integrations is not unset:
            kwargs["integrations"] = integrations
        if org is not unset:
            kwargs["org"] = org
        if tags is not unset:
            kwargs["tags"] = tags
        super().__init__(kwargs)

        self_.info = info
        self_.schema_version = schema_version
