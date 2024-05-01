# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import List, Union, TYPE_CHECKING

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    unset,
    UnsetType,
)


if TYPE_CHECKING:
    from datadog_api_client.v2.model.security_monitoring_rule_response import SecurityMonitoringRuleResponse
    from datadog_api_client.v2.model.response_meta_attributes import ResponseMetaAttributes
    from datadog_api_client.v2.model.security_monitoring_standard_rule_response import (
        SecurityMonitoringStandardRuleResponse,
    )
    from datadog_api_client.v2.model.security_monitoring_signal_rule_response import (
        SecurityMonitoringSignalRuleResponse,
    )


class SecurityMonitoringListRulesResponse(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.security_monitoring_rule_response import SecurityMonitoringRuleResponse
        from datadog_api_client.v2.model.response_meta_attributes import ResponseMetaAttributes

        return {
            "data": ([SecurityMonitoringRuleResponse],),
            "meta": (ResponseMetaAttributes,),
        }

    attribute_map = {
        "data": "data",
        "meta": "meta",
    }

    def __init__(
        self_,
        data: Union[
            List[
                Union[
                    SecurityMonitoringRuleResponse,
                    SecurityMonitoringStandardRuleResponse,
                    SecurityMonitoringSignalRuleResponse,
                ]
            ],
            UnsetType,
        ] = unset,
        meta: Union[ResponseMetaAttributes, UnsetType] = unset,
        **kwargs,
    ):
        """
        List of rules.

        :param data: Array containing the list of rules.
        :type data: [SecurityMonitoringRuleResponse], optional

        :param meta: Object describing meta attributes of response.
        :type meta: ResponseMetaAttributes, optional
        """
        if data is not unset:
            kwargs["data"] = data
        if meta is not unset:
            kwargs["meta"] = meta
        super().__init__(kwargs)
