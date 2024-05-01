# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Union

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    unset,
    UnsetType,
)


class SensitiveDataScannerMeta(ModelNormal):
    validations = {
        "version": {
            "inclusive_minimum": 0,
        },
    }

    @cached_property
    def openapi_types(_):
        return {
            "count_limit": (int,),
            "group_count_limit": (int,),
            "has_highlight_enabled": (bool,),
            "is_pci_compliant": (bool,),
            "version": (int,),
        }

    attribute_map = {
        "count_limit": "count_limit",
        "group_count_limit": "group_count_limit",
        "has_highlight_enabled": "has_highlight_enabled",
        "is_pci_compliant": "is_pci_compliant",
        "version": "version",
    }

    def __init__(
        self_,
        count_limit: Union[int, UnsetType] = unset,
        group_count_limit: Union[int, UnsetType] = unset,
        has_highlight_enabled: Union[bool, UnsetType] = unset,
        is_pci_compliant: Union[bool, UnsetType] = unset,
        version: Union[int, UnsetType] = unset,
        **kwargs,
    ):
        """
        Meta response containing information about the API.

        :param count_limit: Maximum number of scanning rules allowed for the org.
        :type count_limit: int, optional

        :param group_count_limit: Maximum number of scanning groups allowed for the org.
        :type group_count_limit: int, optional

        :param has_highlight_enabled: Whether or not scanned events are highlighted in Logs or RUM for the org.
        :type has_highlight_enabled: bool, optional

        :param is_pci_compliant: Whether or not the org is compliant to the payment card industry standard.
        :type is_pci_compliant: bool, optional

        :param version: Version of the API.
        :type version: int, optional
        """
        if count_limit is not unset:
            kwargs["count_limit"] = count_limit
        if group_count_limit is not unset:
            kwargs["group_count_limit"] = group_count_limit
        if has_highlight_enabled is not unset:
            kwargs["has_highlight_enabled"] = has_highlight_enabled
        if is_pci_compliant is not unset:
            kwargs["is_pci_compliant"] = is_pci_compliant
        if version is not unset:
            kwargs["version"] = version
        super().__init__(kwargs)
