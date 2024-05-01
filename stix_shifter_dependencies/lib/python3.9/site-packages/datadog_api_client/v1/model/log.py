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
    from datadog_api_client.v1.model.log_content import LogContent


class Log(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.log_content import LogContent

        return {
            "content": (LogContent,),
            "id": (str,),
        }

    attribute_map = {
        "content": "content",
        "id": "id",
    }

    def __init__(self_, content: Union[LogContent, UnsetType] = unset, id: Union[str, UnsetType] = unset, **kwargs):
        """
        Object describing a log after being processed and stored by Datadog.

        :param content: JSON object containing all log attributes and their associated values.
        :type content: LogContent, optional

        :param id: Unique ID of the Log.
        :type id: str, optional
        """
        if content is not unset:
            kwargs["content"] = content
        if id is not unset:
            kwargs["id"] = id
        super().__init__(kwargs)
