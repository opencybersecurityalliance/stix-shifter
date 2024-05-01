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
    from datadog_api_client.v2.model.opsgenie_service_region_type import OpsgenieServiceRegionType


class OpsgenieServiceCreateAttributes(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.opsgenie_service_region_type import OpsgenieServiceRegionType

        return {
            "custom_url": (str,),
            "name": (str,),
            "opsgenie_api_key": (str,),
            "region": (OpsgenieServiceRegionType,),
        }

    attribute_map = {
        "custom_url": "custom_url",
        "name": "name",
        "opsgenie_api_key": "opsgenie_api_key",
        "region": "region",
    }

    def __init__(
        self_,
        name: str,
        opsgenie_api_key: str,
        region: OpsgenieServiceRegionType,
        custom_url: Union[str, UnsetType] = unset,
        **kwargs,
    ):
        """
        The Opsgenie service attributes for a create request.

        :param custom_url: The custom URL for a custom region.
        :type custom_url: str, optional

        :param name: The name for the Opsgenie service.
        :type name: str

        :param opsgenie_api_key: The Opsgenie API key for your Opsgenie service.
        :type opsgenie_api_key: str

        :param region: The region for the Opsgenie service.
        :type region: OpsgenieServiceRegionType
        """
        if custom_url is not unset:
            kwargs["custom_url"] = custom_url
        super().__init__(kwargs)

        self_.name = name
        self_.opsgenie_api_key = opsgenie_api_key
        self_.region = region
