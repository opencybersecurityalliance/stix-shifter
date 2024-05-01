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


class SensitiveDataScannerMetaVersionOnly(ModelNormal):
    validations = {
        "version": {
            "inclusive_minimum": 0,
        },
    }

    @cached_property
    def openapi_types(_):
        return {
            "version": (int,),
        }

    attribute_map = {
        "version": "version",
    }

    def __init__(self_, version: Union[int, UnsetType] = unset, **kwargs):
        """
        Meta payload containing information about the API.

        :param version: Version of the API (optional).
        :type version: int, optional
        """
        if version is not unset:
            kwargs["version"] = version
        super().__init__(kwargs)
