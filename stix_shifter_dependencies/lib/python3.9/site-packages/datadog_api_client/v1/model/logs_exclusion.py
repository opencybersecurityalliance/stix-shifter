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
    from datadog_api_client.v1.model.logs_exclusion_filter import LogsExclusionFilter


class LogsExclusion(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.logs_exclusion_filter import LogsExclusionFilter

        return {
            "filter": (LogsExclusionFilter,),
            "is_enabled": (bool,),
            "name": (str,),
        }

    attribute_map = {
        "filter": "filter",
        "is_enabled": "is_enabled",
        "name": "name",
    }

    def __init__(
        self_,
        name: str,
        filter: Union[LogsExclusionFilter, UnsetType] = unset,
        is_enabled: Union[bool, UnsetType] = unset,
        **kwargs,
    ):
        """
        Represents the index exclusion filter object from configuration API.

        :param filter: Exclusion filter is defined by a query, a sampling rule, and a active/inactive toggle.
        :type filter: LogsExclusionFilter, optional

        :param is_enabled: Whether or not the exclusion filter is active.
        :type is_enabled: bool, optional

        :param name: Name of the index exclusion filter.
        :type name: str
        """
        if filter is not unset:
            kwargs["filter"] = filter
        if is_enabled is not unset:
            kwargs["is_enabled"] = is_enabled
        super().__init__(kwargs)

        self_.name = name
