# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import List, Union

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    none_type,
    unset,
    UnsetType,
)


class CloudConfigurationRuleComplianceSignalOptions(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "user_activation_status": (bool, none_type),
            "user_group_by_fields": ([str], none_type),
        }

    attribute_map = {
        "user_activation_status": "userActivationStatus",
        "user_group_by_fields": "userGroupByFields",
    }

    def __init__(
        self_,
        user_activation_status: Union[bool, none_type, UnsetType] = unset,
        user_group_by_fields: Union[List[str], none_type, UnsetType] = unset,
        **kwargs,
    ):
        """
        How to generate compliance signals. Useful for cloud_configuration rules only.

        :param user_activation_status: Whether signals will be sent.
        :type user_activation_status: bool, none_type, optional

        :param user_group_by_fields: Fields to use to group findings by when sending signals.
        :type user_group_by_fields: [str], none_type, optional
        """
        if user_activation_status is not unset:
            kwargs["user_activation_status"] = user_activation_status
        if user_group_by_fields is not unset:
            kwargs["user_group_by_fields"] = user_group_by_fields
        super().__init__(kwargs)
