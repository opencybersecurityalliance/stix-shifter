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


class SecurityFilterMeta(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "warning": (str,),
        }

    attribute_map = {
        "warning": "warning",
    }

    def __init__(self_, warning: Union[str, UnsetType] = unset, **kwargs):
        """
        Optional metadata associated to the response.

        :param warning: A warning message.
        :type warning: str, optional
        """
        if warning is not unset:
            kwargs["warning"] = warning
        super().__init__(kwargs)
