# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Union

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    datetime,
    unset,
    UnsetType,
)


class AuthNMappingAttributes(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "attribute_key": (str,),
            "attribute_value": (str,),
            "created_at": (datetime,),
            "modified_at": (datetime,),
            "saml_assertion_attribute_id": (str,),
        }

    attribute_map = {
        "attribute_key": "attribute_key",
        "attribute_value": "attribute_value",
        "created_at": "created_at",
        "modified_at": "modified_at",
        "saml_assertion_attribute_id": "saml_assertion_attribute_id",
    }
    read_only_vars = {
        "created_at",
        "modified_at",
    }

    def __init__(
        self_,
        attribute_key: Union[str, UnsetType] = unset,
        attribute_value: Union[str, UnsetType] = unset,
        created_at: Union[datetime, UnsetType] = unset,
        modified_at: Union[datetime, UnsetType] = unset,
        saml_assertion_attribute_id: Union[str, UnsetType] = unset,
        **kwargs,
    ):
        """
        Attributes of AuthN Mapping.

        :param attribute_key: Key portion of a key/value pair of the attribute sent from the Identity Provider.
        :type attribute_key: str, optional

        :param attribute_value: Value portion of a key/value pair of the attribute sent from the Identity Provider.
        :type attribute_value: str, optional

        :param created_at: Creation time of the AuthN Mapping.
        :type created_at: datetime, optional

        :param modified_at: Time of last AuthN Mapping modification.
        :type modified_at: datetime, optional

        :param saml_assertion_attribute_id: The ID of the SAML assertion attribute.
        :type saml_assertion_attribute_id: str, optional
        """
        if attribute_key is not unset:
            kwargs["attribute_key"] = attribute_key
        if attribute_value is not unset:
            kwargs["attribute_value"] = attribute_value
        if created_at is not unset:
            kwargs["created_at"] = created_at
        if modified_at is not unset:
            kwargs["modified_at"] = modified_at
        if saml_assertion_attribute_id is not unset:
            kwargs["saml_assertion_attribute_id"] = saml_assertion_attribute_id
        super().__init__(kwargs)
