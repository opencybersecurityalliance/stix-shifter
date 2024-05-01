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


class AWSAccountCreateResponse(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "external_id": (str,),
        }

    attribute_map = {
        "external_id": "external_id",
    }

    def __init__(self_, external_id: Union[str, UnsetType] = unset, **kwargs):
        """
        The Response returned by the AWS Create Account call.

        :param external_id: AWS external_id.
        :type external_id: str, optional
        """
        if external_id is not unset:
            kwargs["external_id"] = external_id
        super().__init__(kwargs)
