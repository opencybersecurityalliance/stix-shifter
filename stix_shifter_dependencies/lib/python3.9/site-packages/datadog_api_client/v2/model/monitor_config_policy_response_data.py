# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Union, TYPE_CHECKING

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    unset,
    UnsetType,
)


if TYPE_CHECKING:
    from datadog_api_client.v2.model.monitor_config_policy_attribute_response import (
        MonitorConfigPolicyAttributeResponse,
    )
    from datadog_api_client.v2.model.monitor_config_policy_resource_type import MonitorConfigPolicyResourceType


class MonitorConfigPolicyResponseData(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.monitor_config_policy_attribute_response import (
            MonitorConfigPolicyAttributeResponse,
        )
        from datadog_api_client.v2.model.monitor_config_policy_resource_type import MonitorConfigPolicyResourceType

        return {
            "attributes": (MonitorConfigPolicyAttributeResponse,),
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
        attributes: Union[MonitorConfigPolicyAttributeResponse, UnsetType] = unset,
        id: Union[str, UnsetType] = unset,
        type: Union[MonitorConfigPolicyResourceType, UnsetType] = unset,
        **kwargs,
    ):
        """
        A monitor configuration policy data.

        :param attributes: Policy and policy type for a monitor configuration policy.
        :type attributes: MonitorConfigPolicyAttributeResponse, optional

        :param id: ID of this monitor configuration policy.
        :type id: str, optional

        :param type: Monitor configuration policy resource type.
        :type type: MonitorConfigPolicyResourceType, optional
        """
        if attributes is not unset:
            kwargs["attributes"] = attributes
        if id is not unset:
            kwargs["id"] = id
        if type is not unset:
            kwargs["type"] = type
        super().__init__(kwargs)
