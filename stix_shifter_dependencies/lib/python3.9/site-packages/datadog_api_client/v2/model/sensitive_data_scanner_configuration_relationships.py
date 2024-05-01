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
    from datadog_api_client.v2.model.sensitive_data_scanner_group_list import SensitiveDataScannerGroupList


class SensitiveDataScannerConfigurationRelationships(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.sensitive_data_scanner_group_list import SensitiveDataScannerGroupList

        return {
            "groups": (SensitiveDataScannerGroupList,),
        }

    attribute_map = {
        "groups": "groups",
    }

    def __init__(self_, groups: Union[SensitiveDataScannerGroupList, UnsetType] = unset, **kwargs):
        """
        Relationships of the configuration.

        :param groups: List of groups, ordered.
        :type groups: SensitiveDataScannerGroupList, optional
        """
        if groups is not unset:
            kwargs["groups"] = groups
        super().__init__(kwargs)
