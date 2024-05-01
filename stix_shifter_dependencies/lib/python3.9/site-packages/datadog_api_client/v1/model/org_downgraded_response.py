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


class OrgDowngradedResponse(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "message": (str,),
        }

    attribute_map = {
        "message": "message",
    }

    def __init__(self_, message: Union[str, UnsetType] = unset, **kwargs):
        """
        Status of downgrade

        :param message: Information pertaining to the downgraded child organization.
        :type message: str, optional
        """
        if message is not unset:
            kwargs["message"] = message
        super().__init__(kwargs)
