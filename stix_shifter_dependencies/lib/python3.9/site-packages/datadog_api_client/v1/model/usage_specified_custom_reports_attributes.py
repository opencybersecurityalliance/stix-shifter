# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import List, Union

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    unset,
    UnsetType,
)


class UsageSpecifiedCustomReportsAttributes(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "computed_on": (str,),
            "end_date": (str,),
            "location": (str,),
            "size": (int,),
            "start_date": (str,),
            "tags": ([str],),
        }

    attribute_map = {
        "computed_on": "computed_on",
        "end_date": "end_date",
        "location": "location",
        "size": "size",
        "start_date": "start_date",
        "tags": "tags",
    }

    def __init__(
        self_,
        computed_on: Union[str, UnsetType] = unset,
        end_date: Union[str, UnsetType] = unset,
        location: Union[str, UnsetType] = unset,
        size: Union[int, UnsetType] = unset,
        start_date: Union[str, UnsetType] = unset,
        tags: Union[List[str], UnsetType] = unset,
        **kwargs,
    ):
        """
        The response containing attributes for specified custom reports.

        :param computed_on: The date the specified custom report was computed.
        :type computed_on: str, optional

        :param end_date: The ending date of specified custom report.
        :type end_date: str, optional

        :param location: A downloadable file for the specified custom reporting file.
        :type location: str, optional

        :param size: size
        :type size: int, optional

        :param start_date: The starting date of specified custom report.
        :type start_date: str, optional

        :param tags: A list of tags to apply to specified custom reports.
        :type tags: [str], optional
        """
        if computed_on is not unset:
            kwargs["computed_on"] = computed_on
        if end_date is not unset:
            kwargs["end_date"] = end_date
        if location is not unset:
            kwargs["location"] = location
        if size is not unset:
            kwargs["size"] = size
        if start_date is not unset:
            kwargs["start_date"] = start_date
        if tags is not unset:
            kwargs["tags"] = tags
        super().__init__(kwargs)
