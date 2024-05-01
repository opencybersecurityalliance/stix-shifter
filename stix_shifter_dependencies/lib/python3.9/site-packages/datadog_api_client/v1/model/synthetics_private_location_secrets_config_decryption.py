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


class SyntheticsPrivateLocationSecretsConfigDecryption(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "key": (str,),
        }

    attribute_map = {
        "key": "key",
    }
    read_only_vars = {
        "key",
    }

    def __init__(self_, key: Union[str, UnsetType] = unset, **kwargs):
        """
        Private key for the private location.

        :param key: Private key for the private location.
        :type key: str, optional
        """
        if key is not unset:
            kwargs["key"] = key
        super().__init__(kwargs)
