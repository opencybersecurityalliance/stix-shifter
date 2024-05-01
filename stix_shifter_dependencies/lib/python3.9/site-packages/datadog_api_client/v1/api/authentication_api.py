# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Any, Dict

from datadog_api_client.api_client import ApiClient, Endpoint as _Endpoint
from datadog_api_client.configuration import Configuration
from datadog_api_client.v1.model.authentication_validation_response import AuthenticationValidationResponse


class AuthenticationApi:
    """
    All requests to Datadog’s API must be authenticated.
    Requests that write data require reporting access and require an ``API key``.
    Requests that read data require full access and also require an ``application key``.

    **Note:** All Datadog API clients are configured by default to consume Datadog US site APIs.
    If you are on the Datadog EU site, set the environment variable ``DATADOG_HOST`` to
    ``https://api.datadoghq.eu`` or override this value directly when creating your client.

    `Manage your account’s API and application keys <https://app.datadoghq.com/account/settings#api>`_.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient(Configuration())
        self.api_client = api_client

        self._validate_endpoint = _Endpoint(
            settings={
                "response_type": (AuthenticationValidationResponse,),
                "auth": ["apiKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v1/validate",
                "operation_id": "validate",
                "http_method": "GET",
                "version": "v1",
                "servers": None,
            },
            params_map={},
            headers_map={
                "accept": ["application/json"],
                "content_type": [],
            },
            api_client=api_client,
        )

    def validate(
        self,
    ) -> AuthenticationValidationResponse:
        """Validate API key.

        Check if the API key (not the APP key) is valid. If invalid, a 403 is returned.

        :rtype: AuthenticationValidationResponse
        """
        kwargs: Dict[str, Any] = {}
        return self._validate_endpoint.call_with_http_info(**kwargs)
