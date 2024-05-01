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
    from datadog_api_client.v1.model.host_map_request import HostMapRequest


class HostMapWidgetDefinitionRequests(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.host_map_request import HostMapRequest

        return {
            "fill": (HostMapRequest,),
            "size": (HostMapRequest,),
        }

    attribute_map = {
        "fill": "fill",
        "size": "size",
    }

    def __init__(
        self_, fill: Union[HostMapRequest, UnsetType] = unset, size: Union[HostMapRequest, UnsetType] = unset, **kwargs
    ):
        """
        List of definitions.

        :param fill: Updated host map.
        :type fill: HostMapRequest, optional

        :param size: Updated host map.
        :type size: HostMapRequest, optional
        """
        if fill is not unset:
            kwargs["fill"] = fill
        if size is not unset:
            kwargs["size"] = size
        super().__init__(kwargs)
