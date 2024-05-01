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
    from datadog_api_client.v1.model.synthetics_basic_auth_oauth_token_api_authentication import (
        SyntheticsBasicAuthOauthTokenApiAuthentication,
    )
    from datadog_api_client.v1.model.synthetics_basic_auth_oauth_rop_type import SyntheticsBasicAuthOauthROPType


class SyntheticsBasicAuthOauthROP(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.synthetics_basic_auth_oauth_token_api_authentication import (
            SyntheticsBasicAuthOauthTokenApiAuthentication,
        )
        from datadog_api_client.v1.model.synthetics_basic_auth_oauth_rop_type import SyntheticsBasicAuthOauthROPType

        return {
            "access_token_url": (str,),
            "audience": (str,),
            "client_id": (str,),
            "client_secret": (str,),
            "password": (str,),
            "resource": (str,),
            "scope": (str,),
            "token_api_authentication": (SyntheticsBasicAuthOauthTokenApiAuthentication,),
            "type": (SyntheticsBasicAuthOauthROPType,),
            "username": (str,),
        }

    attribute_map = {
        "access_token_url": "accessTokenUrl",
        "audience": "audience",
        "client_id": "clientId",
        "client_secret": "clientSecret",
        "password": "password",
        "resource": "resource",
        "scope": "scope",
        "token_api_authentication": "tokenApiAuthentication",
        "type": "type",
        "username": "username",
    }

    def __init__(
        self_,
        access_token_url: str,
        password: str,
        token_api_authentication: SyntheticsBasicAuthOauthTokenApiAuthentication,
        username: str,
        audience: Union[str, UnsetType] = unset,
        client_id: Union[str, UnsetType] = unset,
        client_secret: Union[str, UnsetType] = unset,
        resource: Union[str, UnsetType] = unset,
        scope: Union[str, UnsetType] = unset,
        type: Union[SyntheticsBasicAuthOauthROPType, UnsetType] = unset,
        **kwargs,
    ):
        """
        Object to handle ``oauth rop`` authentication when performing the test.

        :param access_token_url: Access token URL to use when performing the authentication.
        :type access_token_url: str

        :param audience: Audience to use when performing the authentication.
        :type audience: str, optional

        :param client_id: Client ID to use when performing the authentication.
        :type client_id: str, optional

        :param client_secret: Client secret to use when performing the authentication.
        :type client_secret: str, optional

        :param password: Password to use when performing the authentication.
        :type password: str

        :param resource: Resource to use when performing the authentication.
        :type resource: str, optional

        :param scope: Scope to use when performing the authentication.
        :type scope: str, optional

        :param token_api_authentication: Type of token to use when performing the authentication.
        :type token_api_authentication: SyntheticsBasicAuthOauthTokenApiAuthentication

        :param type: The type of basic authentication to use when performing the test.
        :type type: SyntheticsBasicAuthOauthROPType, optional

        :param username: Username to use when performing the authentication.
        :type username: str
        """
        if audience is not unset:
            kwargs["audience"] = audience
        if client_id is not unset:
            kwargs["client_id"] = client_id
        if client_secret is not unset:
            kwargs["client_secret"] = client_secret
        if resource is not unset:
            kwargs["resource"] = resource
        if scope is not unset:
            kwargs["scope"] = scope
        if type is not unset:
            kwargs["type"] = type
        super().__init__(kwargs)

        self_.access_token_url = access_token_url
        self_.password = password
        self_.token_api_authentication = token_api_authentication
        self_.username = username
