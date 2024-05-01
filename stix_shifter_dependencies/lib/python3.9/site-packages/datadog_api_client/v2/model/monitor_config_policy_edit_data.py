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
    from datadog_api_client.v2.model.monitor_config_policy_attribute_edit_request import (
        MonitorConfigPolicyAttributeEditRequest,
    )
    from datadog_api_client.v2.model.monitor_config_policy_resource_type import MonitorConfigPolicyResourceType


class MonitorConfigPolicyEditData(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.monitor_config_policy_attribute_edit_request import (
            MonitorConfigPolicyAttributeEditRequest,
        )
        from datadog_api_client.v2.model.monitor_config_policy_resource_type import MonitorConfigPolicyResourceType

        return {
            "attributes": (MonitorConfigPolicyAttributeEditRequest,),
            "id": (str,),
            "type": (MonitorConfigPolicyResourceType,),
        }

    attribute_map = {
        "attributes": "attributes",
        "id": "id",
        "type": "type",
    }

    def __init__(
        self_,
        attributes: MonitorConfigPolicyAttributeEditRequest,
        id: str,
        type: MonitorConfigPolicyResourceType,
        **kwargs,
    ):
        """
        A monitor configuration policy data.

        :param attributes: Policy and policy type for a monitor configuration policy.
        :type attributes: MonitorConfigPolicyAttributeEditRequest

        :param id: ID of this monitor configuration policy.
        :type id: str

        :param type: Monitor configuration policy resource type.
        :type type: MonitorConfigPolicyResourceType
        """
        super().__init__(kwargs)

        self_.attributes = attributes
        self_.id = id
        self_.type = type
