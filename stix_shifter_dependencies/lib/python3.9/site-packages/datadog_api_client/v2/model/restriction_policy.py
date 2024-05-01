# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import TYPE_CHECKING

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
)


if TYPE_CHECKING:
    from datadog_api_client.v2.model.restriction_policy_attributes import RestrictionPolicyAttributes
    from datadog_api_client.v2.model.restriction_policy_type import RestrictionPolicyType


class RestrictionPolicy(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.restriction_policy_attributes import RestrictionPolicyAttributes
        from datadog_api_client.v2.model.restriction_policy_type import RestrictionPolicyType

        return {
            "attributes": (RestrictionPolicyAttributes,),
            "id": (str,),
            "type": (RestrictionPolicyType,),
        }

    attribute_map = {
        "attributes": "attributes",
        "id": "id",
        "type": "type",
    }

    def __init__(self_, attributes: RestrictionPolicyAttributes, id: str, type: RestrictionPolicyType, **kwargs):
        """
        Restriction policy object.

        :param attributes: Restriction policy attributes.
        :type attributes: RestrictionPolicyAttributes

        :param id: The identifier, always equivalent to the value specified in the ``resource_id`` path parameter.
        :type id: str

        :param type: Restriction policy type.
        :type type: RestrictionPolicyType
        """
        super().__init__(kwargs)

        self_.attributes = attributes
        self_.id = id
        self_.type = type
