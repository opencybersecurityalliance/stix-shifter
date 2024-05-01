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


class IncidentTimelineCellMarkdownCreateAttributesContent(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "content": (str,),
        }

    attribute_map = {
        "content": "content",
    }

    def __init__(self_, content: Union[str, UnsetType] = unset, **kwargs):
        """
        The Markdown timeline cell contents.

        :param content: The Markdown content of the cell.
        :type content: str, optional
        """
        if content is not unset:
            kwargs["content"] = content
        super().__init__(kwargs)
