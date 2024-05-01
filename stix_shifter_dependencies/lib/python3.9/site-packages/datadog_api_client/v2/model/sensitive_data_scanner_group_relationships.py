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
    from datadog_api_client.v2.model.sensitive_data_scanner_configuration_data import (
        SensitiveDataScannerConfigurationData,
    )
    from datadog_api_client.v2.model.sensitive_data_scanner_rule_data import SensitiveDataScannerRuleData


class SensitiveDataScannerGroupRelationships(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.sensitive_data_scanner_configuration_data import (
            SensitiveDataScannerConfigurationData,
        )
        from datadog_api_client.v2.model.sensitive_data_scanner_rule_data import SensitiveDataScannerRuleData

        return {
            "configuration": (SensitiveDataScannerConfigurationData,),
            "rules": (SensitiveDataScannerRuleData,),
        }

    attribute_map = {
        "configuration": "configuration",
        "rules": "rules",
    }

    def __init__(
        self_,
        configuration: Union[SensitiveDataScannerConfigurationData, UnsetType] = unset,
        rules: Union[SensitiveDataScannerRuleData, UnsetType] = unset,
        **kwargs,
    ):
        """
        Relationships of the group.

        :param configuration: A Sensitive Data Scanner configuration data.
        :type configuration: SensitiveDataScannerConfigurationData, optional

        :param rules: Rules included in the group.
        :type rules: SensitiveDataScannerRuleData, optional
        """
        if configuration is not unset:
            kwargs["configuration"] = configuration
        if rules is not unset:
            kwargs["rules"] = rules
        super().__init__(kwargs)
