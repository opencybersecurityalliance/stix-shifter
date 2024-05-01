# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Union

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    unset,
    UnsetType,
)


class ServiceDefinitionV2Doc(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "name": (str,),
            "provider": (str,),
            "url": (str,),
        }

    attribute_map = {
        "name": "name",
        "provider": "provider",
        "url": "url",
    }

    def __init__(self_, name: str, url: str, provider: Union[str, UnsetType] = unset, **kwargs):
        """
        Service documents.

        :param name: Document name.
        :type name: str

        :param provider: Document provider.
        :type provider: str, optional

        :param url: Document URL.
        :type url: str
        """
        if provider is not unset:
            kwargs["provider"] = provider
        super().__init__(kwargs)

        self_.name = name
        self_.url = url
