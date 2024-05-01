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


class ServiceDefinitionV2Dot1Pagerduty(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "service_url": (str,),
        }

    attribute_map = {
        "service_url": "service-url",
    }

    def __init__(self_, service_url: Union[str, UnsetType] = unset, **kwargs):
        """
        PagerDuty integration for the service.

        :param service_url: PagerDuty service url.
        :type service_url: str, optional
        """
        if service_url is not unset:
            kwargs["service_url"] = service_url
        super().__init__(kwargs)
