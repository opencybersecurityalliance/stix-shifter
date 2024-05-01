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
    from datadog_api_client.v2.model.sensitive_data_scanner_group_data import SensitiveDataScannerGroupData
    from datadog_api_client.v2.model.sensitive_data_scanner_standard_pattern_data import (
        SensitiveDataScannerStandardPatternData,
    )


class SensitiveDataScannerRuleRelationships(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.sensitive_data_scanner_group_data import SensitiveDataScannerGroupData
        from datadog_api_client.v2.model.sensitive_data_scanner_standard_pattern_data import (
            SensitiveDataScannerStandardPatternData,
        )

        return {
            "group": (SensitiveDataScannerGroupData,),
            "standard_pattern": (SensitiveDataScannerStandardPatternData,),
        }

    attribute_map = {
        "group": "group",
        "standard_pattern": "standard_pattern",
    }

    def __init__(
        self_,
        group: Union[SensitiveDataScannerGroupData, UnsetType] = unset,
        standard_pattern: Union[SensitiveDataScannerStandardPatternData, UnsetType] = unset,
        **kwargs,
    ):
        """
        Relationships of a scanning rule.

        :param group: A scanning group data.
        :type group: SensitiveDataScannerGroupData, optional

        :param standard_pattern: A standard pattern.
        :type standard_pattern: SensitiveDataScannerStandardPatternData, optional
        """
        if group is not unset:
            kwargs["group"] = group
        if standard_pattern is not unset:
            kwargs["standard_pattern"] = standard_pattern
        super().__init__(kwargs)
