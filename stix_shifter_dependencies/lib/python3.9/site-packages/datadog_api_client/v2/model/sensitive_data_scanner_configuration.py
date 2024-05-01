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
    from datadog_api_client.v2.model.sensitive_data_scanner_configuration_type import (
        SensitiveDataScannerConfigurationType,
    )


class SensitiveDataScannerConfiguration(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.sensitive_data_scanner_configuration_type import (
            SensitiveDataScannerConfigurationType,
        )

        return {
            "id": (str,),
            "type": (SensitiveDataScannerConfigurationType,),
        }

    attribute_map = {
        "id": "id",
        "type": "type",
    }

    def __init__(
        self_,
        id: Union[str, UnsetType] = unset,
        type: Union[SensitiveDataScannerConfigurationType, UnsetType] = unset,
        **kwargs,
    ):
        """
        A Sensitive Data Scanner configuration.

        :param id: ID of the configuration.
        :type id: str, optional

        :param type: Sensitive Data Scanner configuration type.
        :type type: SensitiveDataScannerConfigurationType, optional
        """
        if id is not unset:
            kwargs["id"] = id
        if type is not unset:
            kwargs["type"] = type
        super().__init__(kwargs)
