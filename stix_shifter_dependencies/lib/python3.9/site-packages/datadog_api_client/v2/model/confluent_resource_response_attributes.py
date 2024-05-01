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


class ConfluentResourceResponseAttributes(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "resource_type": (str,),
            "tags": ([str],),
        }

    attribute_map = {
        "resource_type": "resource_type",
        "tags": "tags",
    }

    def __init__(self_, resource_type: str, tags: Union[List[str], UnsetType] = unset, **kwargs):
        """
        Model representation of a Confluent Cloud resource.

        :param resource_type: The resource type of the Resource. Can be ``kafka`` , ``connector`` , ``ksql`` , or ``schema_registry``.
        :type resource_type: str

        :param tags: A list of strings representing tags. Can be a single key, or key-value pairs separated by a colon.
        :type tags: [str], optional
        """
        if tags is not unset:
            kwargs["tags"] = tags
        super().__init__(kwargs)

        self_.resource_type = resource_type
