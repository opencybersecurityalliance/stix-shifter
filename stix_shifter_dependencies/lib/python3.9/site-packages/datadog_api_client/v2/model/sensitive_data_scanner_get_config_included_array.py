# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)


class SensitiveDataScannerGetConfigIncludedArray(ModelSimple):
    """
    Included objects from relationships.


    :type value: [SensitiveDataScannerGetConfigIncludedItem]
    """

    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.sensitive_data_scanner_get_config_included_item import (
            SensitiveDataScannerGetConfigIncludedItem,
        )

        return {
            "value": ([SensitiveDataScannerGetConfigIncludedItem],),
        }
