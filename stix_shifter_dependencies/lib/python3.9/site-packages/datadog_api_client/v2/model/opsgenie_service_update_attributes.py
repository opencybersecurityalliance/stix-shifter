# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Union, TYPE_CHECKING

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    none_type,
    unset,
    UnsetType,
)


if TYPE_CHECKING:
    from datadog_api_client.v2.model.opsgenie_service_region_type import OpsgenieServiceRegionType


class OpsgenieServiceUpdateAttributes(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.opsgenie_service_region_type import OpsgenieServiceRegionType

        return {
            "custom_url": (str, none_type),
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
        custom_url: Union[str, none_type, UnsetType] = unset,
        name: Union[str, UnsetType] = unset,
        opsgenie_api_key: Union[str, UnsetType] = unset,
        region: Union[OpsgenieServiceRegionType, UnsetType] = unset,
        **kwargs,
    ):
        """
        The Opsgenie service attributes for an update request.

        :param custom_url: The custom URL for a custom region.
        :type custom_url: str, none_type, optional

        :param name: The name for the Opsgenie service.
        :type name: str, optional

        :param opsgenie_api_key: The Opsgenie API key for your Opsgenie service.
        :type opsgenie_api_key: str, optional

        :param region: The region for the Opsgenie service.
        :type region: OpsgenieServiceRegionType, optional
        """
        if custom_url is not unset:
            kwargs["custom_url"] = custom_url
        if name is not unset:
            kwargs["name"] = name
        if opsgenie_api_key is not unset:
            kwargs["opsgenie_api_key"] = opsgenie_api_key
        if region is not unset:
            kwargs["region"] = region
        super().__init__(kwargs)
