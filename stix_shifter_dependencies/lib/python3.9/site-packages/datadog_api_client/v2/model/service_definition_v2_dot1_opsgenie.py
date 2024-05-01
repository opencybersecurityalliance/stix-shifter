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
    from datadog_api_client.v2.model.service_definition_v2_dot1_opsgenie_region import (
        ServiceDefinitionV2Dot1OpsgenieRegion,
    )


class ServiceDefinitionV2Dot1Opsgenie(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.service_definition_v2_dot1_opsgenie_region import (
            ServiceDefinitionV2Dot1OpsgenieRegion,
        )

        return {
            "region": (ServiceDefinitionV2Dot1OpsgenieRegion,),
            "service_url": (str,),
        }

    attribute_map = {
        "region": "region",
        "service_url": "service-url",
    }

    def __init__(
        self_, service_url: str, region: Union[ServiceDefinitionV2Dot1OpsgenieRegion, UnsetType] = unset, **kwargs
    ):
        """
        Opsgenie integration for the service.

        :param region: Opsgenie instance region.
        :type region: ServiceDefinitionV2Dot1OpsgenieRegion, optional

        :param service_url: Opsgenie service url.
        :type service_url: str
        """
        if region is not unset:
            kwargs["region"] = region
        super().__init__(kwargs)

        self_.service_url = service_url
