# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import List, Union, TYPE_CHECKING

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    unset,
    UnsetType,
)


if TYPE_CHECKING:
    from datadog_api_client.v2.model.fastly_service import FastlyService


class FastlyAccountCreateRequestAttributes(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.fastly_service import FastlyService

        return {
            "api_key": (str,),
            "name": (str,),
            "services": ([FastlyService],),
        }

    attribute_map = {
        "api_key": "api_key",
        "name": "name",
        "services": "services",
    }

    def __init__(self_, api_key: str, name: str, services: Union[List[FastlyService], UnsetType] = unset, **kwargs):
        """
        Attributes object for creating a Fastly account.

        :param api_key: The API key for the Fastly account.
        :type api_key: str

        :param name: The name of the Fastly account.
        :type name: str

        :param services: A list of services belonging to the parent account.
        :type services: [FastlyService], optional
        """
        if services is not unset:
            kwargs["services"] = services
        super().__init__(kwargs)

        self_.api_key = api_key
        self_.name = name
