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
    from datadog_api_client.v1.model.logs_user_agent_parser_type import LogsUserAgentParserType


class LogsUserAgentParser(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.logs_user_agent_parser_type import LogsUserAgentParserType

        return {
            "is_enabled": (bool,),
            "is_encoded": (bool,),
            "name": (str,),
            "sources": ([str],),
            "target": (str,),
            "type": (LogsUserAgentParserType,),
        }

    attribute_map = {
        "is_enabled": "is_enabled",
        "is_encoded": "is_encoded",
        "name": "name",
        "sources": "sources",
        "target": "target",
        "type": "type",
    }

    def __init__(
        self_,
        type: LogsUserAgentParserType,
        is_enabled: Union[bool, UnsetType] = unset,
        is_encoded: Union[bool, UnsetType] = unset,
        name: Union[str, UnsetType] = unset,
        **kwargs,
    ):
        """
        The User-Agent parser takes a User-Agent attribute and extracts the OS, browser, device, and other user data.
        It recognizes major bots like the Google Bot, Yahoo Slurp, and Bing.

        :param is_enabled: Whether or not the processor is enabled.
        :type is_enabled: bool, optional

        :param is_encoded: Define if the source attribute is URL encoded or not.
        :type is_encoded: bool, optional

        :param name: Name of the processor.
        :type name: str, optional

        :param sources: Array of source attributes.
        :type sources: [str]

        :param target: Name of the parent attribute that contains all the extracted details from the ``sources``.
        :type target: str

        :param type: Type of logs User-Agent parser.
        :type type: LogsUserAgentParserType
        """
        if is_enabled is not unset:
            kwargs["is_enabled"] = is_enabled
        if is_encoded is not unset:
            kwargs["is_encoded"] = is_encoded
        if name is not unset:
            kwargs["name"] = name
        super().__init__(kwargs)
        sources = kwargs.get("sources", ["http.useragent"])
        target = kwargs.get("target", "http.useragent_details")

        self_.sources = sources
        self_.target = target
        self_.type = type
