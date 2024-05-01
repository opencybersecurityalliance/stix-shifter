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
    from datadog_api_client.v2.model.authn_mapping import AuthNMapping
    from datadog_api_client.v2.model.authn_mapping_included import AuthNMappingIncluded
    from datadog_api_client.v2.model.saml_assertion_attribute import SAMLAssertionAttribute
    from datadog_api_client.v2.model.role import Role


class AuthNMappingResponse(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.authn_mapping import AuthNMapping
        from datadog_api_client.v2.model.authn_mapping_included import AuthNMappingIncluded

        return {
            "data": (AuthNMapping,),
            "included": ([AuthNMappingIncluded],),
        }

    attribute_map = {
        "data": "data",
        "included": "included",
    }

    def __init__(
        self_,
        data: Union[AuthNMapping, UnsetType] = unset,
        included: Union[List[Union[AuthNMappingIncluded, SAMLAssertionAttribute, Role]], UnsetType] = unset,
        **kwargs,
    ):
        """
        AuthN Mapping response from the API.

        :param data: The AuthN Mapping object returned by API.
        :type data: AuthNMapping, optional

        :param included: Included data in the AuthN Mapping response.
        :type included: [AuthNMappingIncluded], optional
        """
        if data is not unset:
            kwargs["data"] = data
        if included is not unset:
            kwargs["included"] = included
        super().__init__(kwargs)
