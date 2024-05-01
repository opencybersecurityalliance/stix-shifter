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


class ServiceDefinitionV1Info(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "dd_service": (str,),
            "description": (str,),
            "display_name": (str,),
            "service_tier": (str,),
        }

    attribute_map = {
        "dd_service": "dd-service",
        "description": "description",
        "display_name": "display-name",
        "service_tier": "service-tier",
    }

    def __init__(
        self_,
        dd_service: str,
        description: Union[str, UnsetType] = unset,
        display_name: Union[str, UnsetType] = unset,
        service_tier: Union[str, UnsetType] = unset,
        **kwargs,
    ):
        """
        Basic information about a service.

        :param dd_service: Unique identifier of the service. Must be unique across all services and is used to match with a service in Datadog.
        :type dd_service: str

        :param description: A short description of the service.
        :type description: str, optional

        :param display_name: A friendly name of the service.
        :type display_name: str, optional

        :param service_tier: Service tier.
        :type service_tier: str, optional
        """
        if description is not unset:
            kwargs["description"] = description
        if display_name is not unset:
            kwargs["display_name"] = display_name
        if service_tier is not unset:
            kwargs["service_tier"] = service_tier
        super().__init__(kwargs)

        self_.dd_service = dd_service
