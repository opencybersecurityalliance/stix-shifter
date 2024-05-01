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
    from datadog_api_client.v1.model.logs_geo_ip_parser_type import LogsGeoIPParserType


class LogsGeoIPParser(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.logs_geo_ip_parser_type import LogsGeoIPParserType

        return {
            "is_enabled": (bool,),
            "name": (str,),
            "sources": ([str],),
            "target": (str,),
            "type": (LogsGeoIPParserType,),
        }

    attribute_map = {
        "is_enabled": "is_enabled",
        "name": "name",
        "sources": "sources",
        "target": "target",
        "type": "type",
    }

    def __init__(
        self_,
        type: LogsGeoIPParserType,
        is_enabled: Union[bool, UnsetType] = unset,
        name: Union[str, UnsetType] = unset,
        **kwargs,
    ):
        """
        The GeoIP parser takes an IP address attribute and extracts if available
        the Continent, Country, Subdivision, and City information in the target attribute path.

        :param is_enabled: Whether or not the processor is enabled.
        :type is_enabled: bool, optional

        :param name: Name of the processor.
        :type name: str, optional

        :param sources: Array of source attributes.
        :type sources: [str]

        :param target: Name of the parent attribute that contains all the extracted details from the ``sources``.
        :type target: str

        :param type: Type of GeoIP parser.
        :type type: LogsGeoIPParserType
        """
        if is_enabled is not unset:
            kwargs["is_enabled"] = is_enabled
        if name is not unset:
            kwargs["name"] = name
        super().__init__(kwargs)
        sources = kwargs.get("sources", ["network.client.ip"])
        target = kwargs.get("target", "network.client.geoip")

        self_.sources = sources
        self_.target = target
        self_.type = type
