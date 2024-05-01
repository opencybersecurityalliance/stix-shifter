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
    from datadog_api_client.v2.model.sensitive_data_scanner_group_create import SensitiveDataScannerGroupCreate
    from datadog_api_client.v2.model.sensitive_data_scanner_meta_version_only import SensitiveDataScannerMetaVersionOnly


class SensitiveDataScannerGroupCreateRequest(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.sensitive_data_scanner_group_create import SensitiveDataScannerGroupCreate
        from datadog_api_client.v2.model.sensitive_data_scanner_meta_version_only import (
            SensitiveDataScannerMetaVersionOnly,
        )

        return {
            "data": (SensitiveDataScannerGroupCreate,),
            "meta": (SensitiveDataScannerMetaVersionOnly,),
        }

    attribute_map = {
        "data": "data",
        "meta": "meta",
    }

    def __init__(
        self_,
        data: Union[SensitiveDataScannerGroupCreate, UnsetType] = unset,
        meta: Union[SensitiveDataScannerMetaVersionOnly, UnsetType] = unset,
        **kwargs,
    ):
        """
        Create group request.

        :param data: Data related to the creation of a group.
        :type data: SensitiveDataScannerGroupCreate, optional

        :param meta: Meta payload containing information about the API.
        :type meta: SensitiveDataScannerMetaVersionOnly, optional
        """
        if data is not unset:
            kwargs["data"] = data
        if meta is not unset:
            kwargs["meta"] = meta
        super().__init__(kwargs)
