# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import List

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
)


class MonitorConfigPolicyTagPolicyCreateRequest(ModelNormal):
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

    def __init__(self_, tag_key: str, tag_key_required: bool, valid_tag_values: List[str], **kwargs):
        """
        Tag attributes of a monitor configuration policy.

        :param tag_key: The key of the tag.
        :type tag_key: str

        :param tag_key_required: If a tag key is required for monitor creation.
        :type tag_key_required: bool

        :param valid_tag_values: Valid values for the tag.
        :type valid_tag_values: [str]
        """
        super().__init__(kwargs)

        self_.tag_key = tag_key
        self_.tag_key_required = tag_key_required
        self_.valid_tag_values = valid_tag_values
