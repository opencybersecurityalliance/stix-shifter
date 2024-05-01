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
    from datadog_api_client.v1.model.logs_grok_parser_rules import LogsGrokParserRules
    from datadog_api_client.v1.model.logs_grok_parser_type import LogsGrokParserType


class LogsGrokParser(ModelNormal):
    validations = {
        "samples": {
            "max_items": 5,
        },
    }

    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.logs_grok_parser_rules import LogsGrokParserRules
        from datadog_api_client.v1.model.logs_grok_parser_type import LogsGrokParserType

        return {
            "grok": (LogsGrokParserRules,),
            "is_enabled": (bool,),
            "name": (str,),
            "samples": ([str],),
            "source": (str,),
            "type": (LogsGrokParserType,),
        }

    attribute_map = {
        "grok": "grok",
        "is_enabled": "is_enabled",
        "name": "name",
        "samples": "samples",
        "source": "source",
        "type": "type",
    }

    def __init__(
        self_,
        grok: LogsGrokParserRules,
        type: LogsGrokParserType,
        is_enabled: Union[bool, UnsetType] = unset,
        name: Union[str, UnsetType] = unset,
        samples: Union[List[str], UnsetType] = unset,
        **kwargs,
    ):
        """
        Create custom grok rules to parse the full message or `a specific attribute of your raw event <https://docs.datadoghq.com/logs/log_configuration/parsing/#advanced-settings>`_.
        For more information, see the `parsing section <https://docs.datadoghq.com/logs/log_configuration/parsing>`_.

        :param grok: Set of rules for the grok parser.
        :type grok: LogsGrokParserRules

        :param is_enabled: Whether or not the processor is enabled.
        :type is_enabled: bool, optional

        :param name: Name of the processor.
        :type name: str, optional

        :param samples: List of sample logs to test this grok parser.
        :type samples: [str], optional

        :param source: Name of the log attribute to parse.
        :type source: str

        :param type: Type of logs grok parser.
        :type type: LogsGrokParserType
        """
        if is_enabled is not unset:
            kwargs["is_enabled"] = is_enabled
        if name is not unset:
            kwargs["name"] = name
        if samples is not unset:
            kwargs["samples"] = samples
        super().__init__(kwargs)
        source = kwargs.get("source", "message")

        self_.grok = grok
        self_.source = source
        self_.type = type
