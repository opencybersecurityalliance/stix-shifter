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
    from datadog_api_client.v2.model.confluent_resource_response_attributes import ConfluentResourceResponseAttributes


class ConfluentAccountResponseAttributes(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.confluent_resource_response_attributes import (
            ConfluentResourceResponseAttributes,
        )

        return {
            "api_key": (str,),
            "resources": ([ConfluentResourceResponseAttributes],),
            "tags": ([str],),
        }

    attribute_map = {
        "api_key": "api_key",
        "resources": "resources",
        "tags": "tags",
    }

    def __init__(
        self_,
        api_key: str,
        resources: Union[List[ConfluentResourceResponseAttributes], UnsetType] = unset,
        tags: Union[List[str], UnsetType] = unset,
        **kwargs,
    ):
        """
        The attributes of a Confluent account.

        :param api_key: The API key associated with your Confluent account.
        :type api_key: str

        :param resources: A list of Confluent resources associated with the Confluent account.
        :type resources: [ConfluentResourceResponseAttributes], optional

        :param tags: A list of strings representing tags. Can be a single key, or key-value pairs separated by a colon.
        :type tags: [str], optional
        """
        if resources is not unset:
            kwargs["resources"] = resources
        if tags is not unset:
            kwargs["tags"] = tags
        super().__init__(kwargs)

        self_.api_key = api_key
