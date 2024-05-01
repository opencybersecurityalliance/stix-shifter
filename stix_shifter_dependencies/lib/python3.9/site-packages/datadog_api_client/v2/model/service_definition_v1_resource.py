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
    from datadog_api_client.v2.model.service_definition_v1_resource_type import ServiceDefinitionV1ResourceType


class ServiceDefinitionV1Resource(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.service_definition_v1_resource_type import ServiceDefinitionV1ResourceType

        return {
            "name": (str,),
            "type": (ServiceDefinitionV1ResourceType,),
            "url": (str,),
        }

    attribute_map = {
        "name": "name",
        "type": "type",
        "url": "url",
    }

    def __init__(self_, name: str, type: ServiceDefinitionV1ResourceType, url: str, **kwargs):
        """
        Service's external links.

        :param name: Link name.
        :type name: str

        :param type: Link type.
        :type type: ServiceDefinitionV1ResourceType

        :param url: Link URL.
        :type url: str
        """
        super().__init__(kwargs)

        self_.name = name
        self_.type = type
        self_.url = url
