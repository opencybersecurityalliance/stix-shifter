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


class SensitiveDataScannerGroupUpdate(ModelNormal):
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
            "id": (str,),
            "relationships": (SensitiveDataScannerGroupRelationships,),
            "type": (SensitiveDataScannerGroupType,),
        }

    attribute_map = {
        "attributes": "attributes",
        "id": "id",
        "relationships": "relationships",
        "type": "type",
    }

    def __init__(
        self_,
        attributes: Union[SensitiveDataScannerGroupAttributes, UnsetType] = unset,
        id: Union[str, UnsetType] = unset,
        relationships: Union[SensitiveDataScannerGroupRelationships, UnsetType] = unset,
        type: Union[SensitiveDataScannerGroupType, UnsetType] = unset,
        **kwargs,
    ):
        """
        Data related to the update of a group.

        :param attributes: Attributes of the Sensitive Data Scanner group.
        :type attributes: SensitiveDataScannerGroupAttributes, optional

        :param id: ID of the group.
        :type id: str, optional

        :param relationships: Relationships of the group.
        :type relationships: SensitiveDataScannerGroupRelationships, optional

        :param type: Sensitive Data Scanner group type.
        :type type: SensitiveDataScannerGroupType, optional
        """
        if attributes is not unset:
            kwargs["attributes"] = attributes
        if id is not unset:
            kwargs["id"] = id
        if relationships is not unset:
            kwargs["relationships"] = relationships
        if type is not unset:
            kwargs["type"] = type
        super().__init__(kwargs)
