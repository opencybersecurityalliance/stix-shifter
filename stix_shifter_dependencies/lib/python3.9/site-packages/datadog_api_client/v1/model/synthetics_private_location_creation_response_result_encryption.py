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


class SyntheticsPrivateLocationCreationResponseResultEncryption(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "id": (str,),
            "key": (str,),
        }

    attribute_map = {
        "id": "id",
        "key": "key",
    }

    def __init__(self_, id: Union[str, UnsetType] = unset, key: Union[str, UnsetType] = unset, **kwargs):
        """
        Public key for the result encryption.

        :param id: Fingerprint for the encryption key.
        :type id: str, optional

        :param key: Public key for result encryption.
        :type key: str, optional
        """
        if id is not unset:
            kwargs["id"] = id
        if key is not unset:
            kwargs["key"] = key
        super().__init__(kwargs)
