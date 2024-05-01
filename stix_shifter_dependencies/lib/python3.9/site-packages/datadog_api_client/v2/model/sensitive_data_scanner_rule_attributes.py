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
    from datadog_api_client.v2.model.sensitive_data_scanner_text_replacement import SensitiveDataScannerTextReplacement


class SensitiveDataScannerRuleAttributes(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.sensitive_data_scanner_text_replacement import (
            SensitiveDataScannerTextReplacement,
        )

        return {
            "description": (str,),
            "excluded_namespaces": ([str],),
            "is_enabled": (bool,),
            "name": (str,),
            "namespaces": ([str],),
            "pattern": (str,),
            "tags": ([str],),
            "text_replacement": (SensitiveDataScannerTextReplacement,),
        }

    attribute_map = {
        "description": "description",
        "excluded_namespaces": "excluded_namespaces",
        "is_enabled": "is_enabled",
        "name": "name",
        "namespaces": "namespaces",
        "pattern": "pattern",
        "tags": "tags",
        "text_replacement": "text_replacement",
    }

    def __init__(
        self_,
        description: Union[str, UnsetType] = unset,
        excluded_namespaces: Union[List[str], UnsetType] = unset,
        is_enabled: Union[bool, UnsetType] = unset,
        name: Union[str, UnsetType] = unset,
        namespaces: Union[List[str], UnsetType] = unset,
        pattern: Union[str, UnsetType] = unset,
        tags: Union[List[str], UnsetType] = unset,
        text_replacement: Union[SensitiveDataScannerTextReplacement, UnsetType] = unset,
        **kwargs,
    ):
        """
        Attributes of the Sensitive Data Scanner rule.

        :param description: Description of the rule.
        :type description: str, optional

        :param excluded_namespaces: Attributes excluded from the scan. If namespaces is provided, it has to be a sub-path of the namespaces array.
        :type excluded_namespaces: [str], optional

        :param is_enabled: Whether or not the rule is enabled.
        :type is_enabled: bool, optional

        :param name: Name of the rule.
        :type name: str, optional

        :param namespaces: Attributes included in the scan. If namespaces is empty or missing, all attributes except excluded_namespaces are scanned.
            If both are missing the whole event is scanned.
        :type namespaces: [str], optional

        :param pattern: Not included if there is a relationship to a standard pattern.
        :type pattern: str, optional

        :param tags: List of tags.
        :type tags: [str], optional

        :param text_replacement: Object describing how the scanned event will be replaced.
        :type text_replacement: SensitiveDataScannerTextReplacement, optional
        """
        if description is not unset:
            kwargs["description"] = description
        if excluded_namespaces is not unset:
            kwargs["excluded_namespaces"] = excluded_namespaces
        if is_enabled is not unset:
            kwargs["is_enabled"] = is_enabled
        if name is not unset:
            kwargs["name"] = name
        if namespaces is not unset:
            kwargs["namespaces"] = namespaces
        if pattern is not unset:
            kwargs["pattern"] = pattern
        if tags is not unset:
            kwargs["tags"] = tags
        if text_replacement is not unset:
            kwargs["text_replacement"] = text_replacement
        super().__init__(kwargs)
