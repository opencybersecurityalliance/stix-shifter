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
    from datadog_api_client.v2.model.service_definition_v2_dot1_link_type import ServiceDefinitionV2Dot1LinkType


class ServiceDefinitionV2Dot1Link(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.service_definition_v2_dot1_link_type import ServiceDefinitionV2Dot1LinkType

        return {
            "name": (str,),
            "provider": (str,),
            "type": (ServiceDefinitionV2Dot1LinkType,),
            "url": (str,),
        }

    attribute_map = {
        "name": "name",
        "provider": "provider",
        "type": "type",
        "url": "url",
    }

    def __init__(
        self_,
        name: str,
        type: ServiceDefinitionV2Dot1LinkType,
        url: str,
        provider: Union[str, UnsetType] = unset,
        **kwargs,
    ):
        """
        Service's external links.

        :param name: Link name.
        :type name: str

        :param provider: Link provider.
        :type provider: str, optional

        :param type: Link type.
        :type type: ServiceDefinitionV2Dot1LinkType

        :param url: Link URL.
        :type url: str
        """
        if provider is not unset:
            kwargs["provider"] = provider
        super().__init__(kwargs)

        self_.name = name
        self_.type = type
        self_.url = url
