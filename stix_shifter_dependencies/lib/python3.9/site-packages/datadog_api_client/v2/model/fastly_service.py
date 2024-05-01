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


class FastlyService(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "id": (str,),
            "tags": ([str],),
        }

    attribute_map = {
        "id": "id",
        "tags": "tags",
    }

    def __init__(self_, id: str, tags: Union[List[str], UnsetType] = unset, **kwargs):
        """
        The schema representation of a Fastly service.

        :param id: The id of the Fastly service
        :type id: str

        :param tags: A list of tags for the Fastly service.
        :type tags: [str], optional
        """
        if tags is not unset:
            kwargs["tags"] = tags
        super().__init__(kwargs)

        self_.id = id
