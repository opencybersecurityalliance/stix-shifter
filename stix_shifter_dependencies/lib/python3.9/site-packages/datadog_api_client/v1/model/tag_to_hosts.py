# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Dict, List, Union

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    unset,
    UnsetType,
)


class TagToHosts(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "tags": ({str: ([str],)},),
        }

    attribute_map = {
        "tags": "tags",
    }

    def __init__(self_, tags: Union[Dict[str, List[str]], UnsetType] = unset, **kwargs):
        """
        In this object, the key is the tag, the value is a list of host names that are reporting that tag.

        :param tags: A list of tags to apply to the host.
        :type tags: {str: ([str],)}, optional
        """
        if tags is not unset:
            kwargs["tags"] = tags
        super().__init__(kwargs)
