# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import List

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
)


class CloudConfigurationRegoRule(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "policy": (str,),
            "resource_types": ([str],),
        }

    attribute_map = {
        "policy": "policy",
        "resource_types": "resourceTypes",
    }

    def __init__(self_, policy: str, resource_types: List[str], **kwargs):
        """
        Rule details.

        :param policy: The policy written in ``rego`` , see: https://www.openpolicyagent.org/docs/latest/policy-language/
        :type policy: str

        :param resource_types: List of resource types that will be evaluated upon. Must have at least one element.
        :type resource_types: [str]
        """
        super().__init__(kwargs)

        self_.policy = policy
        self_.resource_types = resource_types
