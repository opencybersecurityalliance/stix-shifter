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


class RUMResponsePage(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "after": (str,),
        }

    attribute_map = {
        "after": "after",
    }

    def __init__(self_, after: Union[str, UnsetType] = unset, **kwargs):
        """
        Paging attributes.

        :param after: The cursor to use to get the next results, if any. To make the next request, use the same parameters with the addition of ``page[cursor]``.
        :type after: str, optional
        """
        if after is not unset:
            kwargs["after"] = after
        super().__init__(kwargs)
