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


class AuditLogsResponseLinks(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "next": (str,),
        }

    attribute_map = {
        "next": "next",
    }

    def __init__(self_, next: Union[str, UnsetType] = unset, **kwargs):
        """
        Links attributes.

        :param next: Link for the next set of results. Note that the request can also be made using the
            POST endpoint.
        :type next: str, optional
        """
        if next is not unset:
            kwargs["next"] = next
        super().__init__(kwargs)
