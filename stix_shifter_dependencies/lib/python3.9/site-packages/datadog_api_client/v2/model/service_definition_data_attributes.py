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
    from datadog_api_client.v2.model.service_definition_meta import ServiceDefinitionMeta
    from datadog_api_client.v2.model.service_definition_schema import ServiceDefinitionSchema
    from datadog_api_client.v2.model.service_definition_v1 import ServiceDefinitionV1
    from datadog_api_client.v2.model.service_definition_v2 import ServiceDefinitionV2
    from datadog_api_client.v2.model.service_definition_v2_dot1 import ServiceDefinitionV2Dot1


class ServiceDefinitionDataAttributes(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.service_definition_meta import ServiceDefinitionMeta
        from datadog_api_client.v2.model.service_definition_schema import ServiceDefinitionSchema

        return {
            "meta": (ServiceDefinitionMeta,),
            "schema": (ServiceDefinitionSchema,),
        }

    attribute_map = {
        "meta": "meta",
        "schema": "schema",
    }

    def __init__(
        self_,
        meta: Union[ServiceDefinitionMeta, UnsetType] = unset,
        schema: Union[
            ServiceDefinitionSchema, ServiceDefinitionV1, ServiceDefinitionV2, ServiceDefinitionV2Dot1, UnsetType
        ] = unset,
        **kwargs,
    ):
        """
        Service definition attributes.

        :param meta: Metadata about a service definition.
        :type meta: ServiceDefinitionMeta, optional

        :param schema: Service definition schema.
        :type schema: ServiceDefinitionSchema, optional
        """
        if meta is not unset:
            kwargs["meta"] = meta
        if schema is not unset:
            kwargs["schema"] = schema
        super().__init__(kwargs)
