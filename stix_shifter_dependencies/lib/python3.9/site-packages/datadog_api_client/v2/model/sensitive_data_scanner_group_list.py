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
    from datadog_api_client.v2.model.sensitive_data_scanner_group_item import SensitiveDataScannerGroupItem


class SensitiveDataScannerGroupList(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.sensitive_data_scanner_group_item import SensitiveDataScannerGroupItem

        return {
            "data": ([SensitiveDataScannerGroupItem],),
        }

    attribute_map = {
        "data": "data",
    }

    def __init__(self_, data: Union[List[SensitiveDataScannerGroupItem], UnsetType] = unset, **kwargs):
        """
        List of groups, ordered.

        :param data: List of groups. The order is important.
        :type data: [SensitiveDataScannerGroupItem], optional
        """
        if data is not unset:
            kwargs["data"] = data
        super().__init__(kwargs)
