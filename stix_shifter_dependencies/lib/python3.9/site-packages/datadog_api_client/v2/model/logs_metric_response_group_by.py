# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Union

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    unset,
    UnsetType,
)


class LogsMetricResponseGroupBy(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "path": (str,),
            "tag_name": (str,),
        }

    attribute_map = {
        "path": "path",
        "tag_name": "tag_name",
    }

    def __init__(self_, path: Union[str, UnsetType] = unset, tag_name: Union[str, UnsetType] = unset, **kwargs):
        """
        A group by rule.

        :param path: The path to the value the log-based metric will be aggregated over.
        :type path: str, optional

        :param tag_name: Eventual name of the tag that gets created. By default, the path attribute is used as the tag name.
        :type tag_name: str, optional
        """
        if path is not unset:
            kwargs["path"] = path
        if tag_name is not unset:
            kwargs["tag_name"] = tag_name
        super().__init__(kwargs)
