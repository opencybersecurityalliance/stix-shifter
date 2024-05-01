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
    from datadog_api_client.v2.model.sensitive_data_scanner_rule_type import SensitiveDataScannerRuleType


class SensitiveDataScannerRule(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.sensitive_data_scanner_rule_type import SensitiveDataScannerRuleType

        return {
            "id": (str,),
            "type": (SensitiveDataScannerRuleType,),
        }

    attribute_map = {
        "id": "id",
        "type": "type",
    }

    def __init__(
        self_, id: Union[str, UnsetType] = unset, type: Union[SensitiveDataScannerRuleType, UnsetType] = unset, **kwargs
    ):
        """
        Rule item included in the group.

        :param id: ID of the rule.
        :type id: str, optional

        :param type: Sensitive Data Scanner rule type.
        :type type: SensitiveDataScannerRuleType, optional
        """
        if id is not unset:
            kwargs["id"] = id
        if type is not unset:
            kwargs["type"] = type
        super().__init__(kwargs)
