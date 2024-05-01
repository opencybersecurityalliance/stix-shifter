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
    from datadog_api_client.v2.model.sensitive_data_scanner_meta import SensitiveDataScannerMeta


class SensitiveDataScannerReorderGroupsResponse(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.sensitive_data_scanner_meta import SensitiveDataScannerMeta

        return {
            "meta": (SensitiveDataScannerMeta,),
        }

    attribute_map = {
        "meta": "meta",
    }

    def __init__(self_, meta: Union[SensitiveDataScannerMeta, UnsetType] = unset, **kwargs):
        """
        Group reorder response.

        :param meta: Meta response containing information about the API.
        :type meta: SensitiveDataScannerMeta, optional
        """
        if meta is not unset:
            kwargs["meta"] = meta
        super().__init__(kwargs)
