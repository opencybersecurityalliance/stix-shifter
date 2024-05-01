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
    from datadog_api_client.v2.model.sensitive_data_scanner_group_attributes import SensitiveDataScannerGroupAttributes
    from datadog_api_client.v2.model.sensitive_data_scanner_group_relationships import (
        SensitiveDataScannerGroupRelationships,
    )
    from datadog_api_client.v2.model.sensitive_data_scanner_group_type import SensitiveDataScannerGroupType


class SensitiveDataScannerGroupCreate(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.sensitive_data_scanner_group_attributes import (
            SensitiveDataScannerGroupAttributes,
        )
        from datadog_api_client.v2.model.sensitive_data_scanner_group_relationships import (
            SensitiveDataScannerGroupRelationships,
        )
        from datadog_api_client.v2.model.sensitive_data_scanner_group_type import SensitiveDataScannerGroupType

        return {
            "attributes": (SensitiveDataScannerGroupAttributes,),
            "relationships": (SensitiveDataScannerGroupRelationships,),
            "type": (SensitiveDataScannerGroupType,),
        }

    attribute_map = {
        "attributes": "attributes",
        "relationships": "relationships",
        "type": "type",
    }

    def __init__(
        self_,
        attributes: SensitiveDataScannerGroupAttributes,
        type: SensitiveDataScannerGroupType,
        relationships: Union[SensitiveDataScannerGroupRelationships, UnsetType] = unset,
        **kwargs,
    ):
        """
        Data related to the creation of a group.

        :param attributes: Attributes of the Sensitive Data Scanner group.
        :type attributes: SensitiveDataScannerGroupAttributes

        :param relationships: Relationships of the group.
        :type relationships: SensitiveDataScannerGroupRelationships, optional

        :param type: Sensitive Data Scanner group type.
        :type type: SensitiveDataScannerGroupType
        """
        if relationships is not unset:
            kwargs["relationships"] = relationships
        super().__init__(kwargs)

        self_.attributes = attributes
        self_.type = type
