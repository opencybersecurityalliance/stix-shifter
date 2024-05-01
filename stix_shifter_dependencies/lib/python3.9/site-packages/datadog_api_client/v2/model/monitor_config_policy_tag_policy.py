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


class MonitorConfigPolicyTagPolicy(ModelNormal):
    validations = {
        "tag_key": {
            "max_length": 255,
        },
    }

    @cached_property
    def openapi_types(_):
        return {
            "tag_key": (str,),
            "tag_key_required": (bool,),
            "valid_tag_values": ([str],),
        }

    attribute_map = {
        "tag_key": "tag_key",
        "tag_key_required": "tag_key_required",
        "valid_tag_values": "valid_tag_values",
    }

    def __init__(
        self_,
        tag_key: Union[str, UnsetType] = unset,
        tag_key_required: Union[bool, UnsetType] = unset,
        valid_tag_values: Union[List[str], UnsetType] = unset,
        **kwargs,
    ):
        """
        Tag attributes of a monitor configuration policy.

        :param tag_key: The key of the tag.
        :type tag_key: str, optional

        :param tag_key_required: If a tag key is required for monitor creation.
        :type tag_key_required: bool, optional

        :param valid_tag_values: Valid values for the tag.
        :type valid_tag_values: [str], optional
        """
        if tag_key is not unset:
            kwargs["tag_key"] = tag_key
        if tag_key_required is not unset:
            kwargs["tag_key_required"] = tag_key_required
        if valid_tag_values is not unset:
            kwargs["valid_tag_values"] = valid_tag_values
        super().__init__(kwargs)
