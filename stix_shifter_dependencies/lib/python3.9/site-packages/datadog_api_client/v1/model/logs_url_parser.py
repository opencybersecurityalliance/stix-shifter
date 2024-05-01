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
    from datadog_api_client.v1.model.logs_url_parser_type import LogsURLParserType


class LogsURLParser(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.logs_url_parser_type import LogsURLParserType

        return {
            "is_enabled": (bool,),
            "name": (str,),
            "normalize_ending_slashes": (bool, none_type),
            "sources": ([str],),
            "target": (str,),
            "type": (LogsURLParserType,),
        }

    attribute_map = {
        "is_enabled": "is_enabled",
        "name": "name",
        "normalize_ending_slashes": "normalize_ending_slashes",
        "sources": "sources",
        "target": "target",
        "type": "type",
    }

    def __init__(
        self_,
        type: LogsURLParserType,
        is_enabled: Union[bool, UnsetType] = unset,
        name: Union[str, UnsetType] = unset,
        normalize_ending_slashes: Union[bool, none_type, UnsetType] = unset,
        **kwargs,
    ):
        """
        This processor extracts query parameters and other important parameters from a URL.

        :param is_enabled: Whether or not the processor is enabled.
        :type is_enabled: bool, optional

        :param name: Name of the processor.
        :type name: str, optional

        :param normalize_ending_slashes: Normalize the ending slashes or not.
        :type normalize_ending_slashes: bool, none_type, optional

        :param sources: Array of source attributes.
        :type sources: [str]

        :param target: Name of the parent attribute that contains all the extracted details from the ``sources``.
        :type target: str

        :param type: Type of logs URL parser.
        :type type: LogsURLParserType
        """
        if is_enabled is not unset:
            kwargs["is_enabled"] = is_enabled
        if name is not unset:
            kwargs["name"] = name
        if normalize_ending_slashes is not unset:
            kwargs["normalize_ending_slashes"] = normalize_ending_slashes
        super().__init__(kwargs)
        sources = kwargs.get("sources", ["http.url"])
        target = kwargs.get("target", "http.url_details")

        self_.sources = sources
        self_.target = target
        self_.type = type
