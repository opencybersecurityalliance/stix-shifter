# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelComposed,
    cached_property,
)


class SensitiveDataScannerGetConfigIncludedItem(ModelComposed):
    def __init__(self, **kwargs):
        """
        An object related to the configuration.

        :param attributes: Attributes of the Sensitive Data Scanner rule.
        :type attributes: SensitiveDataScannerRuleAttributes, optional

        :param id: ID of the rule.
        :type id: str, optional

        :param relationships: Relationships of a scanning rule.
        :type relationships: SensitiveDataScannerRuleRelationships, optional

        :param type: Sensitive Data Scanner rule type.
        :type type: SensitiveDataScannerRuleType, optional
        """
        super().__init__(kwargs)

    @cached_property
    def _composed_schemas(_):
        # we need this here to make our import statements work
        # we must store _composed_schemas in here so the code is only run
        # when we invoke this method. If we kept this at the class
        # level we would get an error because the class level
        # code would be run when this module is imported, and these composed
        # classes don't exist yet because their module has not finished
        # loading
        from datadog_api_client.v2.model.sensitive_data_scanner_rule_included_item import (
            SensitiveDataScannerRuleIncludedItem,
        )
        from datadog_api_client.v2.model.sensitive_data_scanner_group_included_item import (
            SensitiveDataScannerGroupIncludedItem,
        )

        return {
            "oneOf": [
                SensitiveDataScannerRuleIncludedItem,
                SensitiveDataScannerGroupIncludedItem,
            ],
        }
