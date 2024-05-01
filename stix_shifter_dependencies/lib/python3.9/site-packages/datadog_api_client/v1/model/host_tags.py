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


class HostTags(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "host": (str,),
            "tags": ([str],),
        }

    attribute_map = {
        "host": "host",
        "tags": "tags",
    }

    def __init__(self_, host: Union[str, UnsetType] = unset, tags: Union[List[str], UnsetType] = unset, **kwargs):
        """
        Set of tags to associate with your host.

        :param host: Your host name.
        :type host: str, optional

        :param tags: A list of tags to apply to the host.
        :type tags: [str], optional
        """
        if host is not unset:
            kwargs["host"] = host
        if tags is not unset:
            kwargs["tags"] = tags
        super().__init__(kwargs)
