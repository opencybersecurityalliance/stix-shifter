# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)


class SensitiveDataScannerStandardPatternsResponse(ModelSimple):
    """
    List Standard patterns response.


    :type value: [SensitiveDataScannerStandardPatternsResponseItem]
    """

    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.sensitive_data_scanner_standard_patterns_response_item import (
            SensitiveDataScannerStandardPatternsResponseItem,
        )

        return {
            "value": ([SensitiveDataScannerStandardPatternsResponseItem],),
        }
