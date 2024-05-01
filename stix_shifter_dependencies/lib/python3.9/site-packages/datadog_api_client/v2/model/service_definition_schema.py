# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelComposed,
    cached_property,
)


class ServiceDefinitionSchema(ModelComposed):
    def __init__(self, **kwargs):
        """
        Service definition schema.

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

        :param contacts: A list of contacts related to the services.
        :type contacts: [ServiceDefinitionV2Contact], optional

        :param dd_service: Unique identifier of the service. Must be unique across all services and is used to match with a service in Datadog.
        :type dd_service: str

        :param dd_team: Experimental feature. A Team handle that matches a Team in the Datadog Teams product.
        :type dd_team: str, optional

        :param docs: A list of documentation related to the services.
        :type docs: [ServiceDefinitionV2Doc], optional

        :param links: A list of links related to the services.
        :type links: [ServiceDefinitionV2Link], optional

        :param repos: A list of code repositories related to the services.
        :type repos: [ServiceDefinitionV2Repo], optional

        :param team: Team that owns the service.
        :type team: str, optional

        :param application: Identifier for a group of related services serving a product feature, which the service is a part of.
        :type application: str, optional

        :param description: A short description of the service.
        :type description: str, optional

        :param lifecycle: The current life cycle phase of the service.
        :type lifecycle: str, optional

        :param tier: Importance of the service.
        :type tier: str, optional
        """
        super().__init__(kwargs)

    @cached_property
    def _composed_schemas(_):
        # we need this here to make our import statements work
        # we must store _composed_schemas in here so the code is only run
        # when we invoke this method. If we kept this at the class
        # level we would get an error because the class level
        # code would be run when this module is imported, and these composed
        # classes don't exist yet because their module has not finished
        # loading
        from datadog_api_client.v2.model.service_definition_v1 import ServiceDefinitionV1
        from datadog_api_client.v2.model.service_definition_v2 import ServiceDefinitionV2
        from datadog_api_client.v2.model.service_definition_v2_dot1 import ServiceDefinitionV2Dot1

        return {
            "oneOf": [
                ServiceDefinitionV1,
                ServiceDefinitionV2,
                ServiceDefinitionV2Dot1,
            ],
        }
