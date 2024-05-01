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
    from datadog_api_client.v1.model.logs_date_remapper_type import LogsDateRemapperType


class LogsDateRemapper(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.logs_date_remapper_type import LogsDateRemapperType

        return {
            "is_enabled": (bool,),
            "name": (str,),
            "sources": ([str],),
            "type": (LogsDateRemapperType,),
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
        type: LogsDateRemapperType,
        is_enabled: Union[bool, UnsetType] = unset,
        name: Union[str, UnsetType] = unset,
        **kwargs,
    ):
        """
        As Datadog receives logs, it timestamps them using the value(s) from any of these default attributes.

        * ``timestamp``
        * ``date``
        * ``_timestamp``
        * ``Timestamp``
        * ``eventTime``
        *
          ``published_date``

          If your logs put their dates in an attribute not in this list,
          use the log date Remapper Processor to define their date attribute as the official log timestamp.
          The recognized date formats are ISO8601, UNIX (the milliseconds EPOCH format), and RFC3164.

          **Note:** If your logs don’t contain any of the default attributes
          and you haven’t defined your own date attribute, Datadog timestamps
          the logs with the date it received them.

          If multiple log date remapper processors can be applied to a given log,
          only the first one (according to the pipelines order) is taken into account.

        :param is_enabled: Whether or not the processor is enabled.
        :type is_enabled: bool, optional

        :param name: Name of the processor.
        :type name: str, optional

        :param sources: Array of source attributes.
        :type sources: [str]

        :param type: Type of logs date remapper.
        :type type: LogsDateRemapperType
        """
        if is_enabled is not unset:
            kwargs["is_enabled"] = is_enabled
        if name is not unset:
            kwargs["name"] = name
        super().__init__(kwargs)

        self_.sources = sources
        self_.type = type
