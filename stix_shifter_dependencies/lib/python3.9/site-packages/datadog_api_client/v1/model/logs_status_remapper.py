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
    from datadog_api_client.v1.model.logs_status_remapper_type import LogsStatusRemapperType


class LogsStatusRemapper(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.logs_status_remapper_type import LogsStatusRemapperType

        return {
            "is_enabled": (bool,),
            "name": (str,),
            "sources": ([str],),
            "type": (LogsStatusRemapperType,),
        }

    attribute_map = {
        "is_enabled": "is_enabled",
        "name": "name",
        "sources": "sources",
        "type": "type",
    }

    def __init__(
        self_,
        sources: List[str],
        type: LogsStatusRemapperType,
        is_enabled: Union[bool, UnsetType] = unset,
        name: Union[str, UnsetType] = unset,
        **kwargs,
    ):
        """
        Use this Processor if you want to assign some attributes as the official status.

        Each incoming status value is mapped as follows.

        * Integers from 0 to 7 map to the Syslog severity standards
        * Strings beginning with ``emerg`` or f (case-insensitive) map to ``emerg`` (0)
        * Strings beginning with ``a`` (case-insensitive) map to ``alert`` (1)
        * Strings beginning with ``c`` (case-insensitive) map to ``critical`` (2)
        * Strings beginning with ``err`` (case-insensitive) map to ``error`` (3)
        * Strings beginning with ``w`` (case-insensitive) map to ``warning`` (4)
        * Strings beginning with ``n`` (case-insensitive) map to ``notice`` (5)
        * Strings beginning with ``i`` (case-insensitive) map to ``info`` (6)
        * Strings beginning with ``d`` , ``trace`` or ``verbose`` (case-insensitive) map to ``debug`` (7)
        * Strings beginning with ``o`` or matching ``OK`` or ``Success`` (case-insensitive) map to OK
        *
          All others map to ``info`` (6)

          **Note:** If multiple log status remapper processors can be applied to a given log,
          only the first one (according to the pipelines order) is taken into account.

        :param is_enabled: Whether or not the processor is enabled.
        :type is_enabled: bool, optional

        :param name: Name of the processor.
        :type name: str, optional

        :param sources: Array of source attributes.
        :type sources: [str]

        :param type: Type of logs status remapper.
        :type type: LogsStatusRemapperType
        """
        if is_enabled is not unset:
            kwargs["is_enabled"] = is_enabled
        if name is not unset:
            kwargs["name"] = name
        super().__init__(kwargs)

        self_.sources = sources
        self_.type = type
