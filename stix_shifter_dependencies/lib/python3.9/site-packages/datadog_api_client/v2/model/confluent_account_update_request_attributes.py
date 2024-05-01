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


class ConfluentAccountUpdateRequestAttributes(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "api_key": (str,),
            "api_secret": (str,),
            "tags": ([str],),
        }

    attribute_map = {
        "api_key": "api_key",
        "api_secret": "api_secret",
        "tags": "tags",
    }

    def __init__(self_, api_key: str, api_secret: str, tags: Union[List[str], UnsetType] = unset, **kwargs):
        """
        Attributes object for updating a Confluent account.

        :param api_key: The API key associated with your Confluent account.
        :type api_key: str

        :param api_secret: The API secret associated with your Confluent account.
        :type api_secret: str

        :param tags: A list of strings representing tags. Can be a single key, or key-value pairs separated by a colon.
        :type tags: [str], optional
        """
        if tags is not unset:
            kwargs["tags"] = tags
        super().__init__(kwargs)

        self_.api_key = api_key
        self_.api_secret = api_secret
