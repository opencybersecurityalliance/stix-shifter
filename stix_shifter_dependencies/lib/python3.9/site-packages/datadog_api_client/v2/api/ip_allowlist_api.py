# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Any, Dict

from datadog_api_client.api_client import ApiClient, Endpoint as _Endpoint
from datadog_api_client.configuration import Configuration
from datadog_api_client.v2.model.ip_allowlist_response import IPAllowlistResponse
from datadog_api_client.v2.model.ip_allowlist_update_request import IPAllowlistUpdateRequest


class IPAllowlistApi:
    """
    The IP allowlist API is used to manage the IP addresses that
    can access the Datadog API and web UI. It does not block
    access to intake APIs or public dashboards.

    This is an enterprise-only feature. Request access by
    contacting Datadog support.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient(Configuration())
        self.api_client = api_client

        self._get_ip_allowlist_endpoint = _Endpoint(
            settings={
                "response_type": (IPAllowlistResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v2/ip_allowlist",
                "operation_id": "get_ip_allowlist",
                "http_method": "GET",
                "version": "v2",
                "servers": None,
            },
            params_map={},
            headers_map={
                "accept": ["application/json"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._update_ip_allowlist_endpoint = _Endpoint(
            settings={
                "response_type": (IPAllowlistResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v2/ip_allowlist",
                "operation_id": "update_ip_allowlist",
                "http_method": "PATCH",
                "version": "v2",
                "servers": None,
            },
            params_map={
                "body": {
                    "required": True,
                    "openapi_types": (IPAllowlistUpdateRequest,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

    def get_ip_allowlist(
        self,
    ) -> IPAllowlistResponse:
        """Get IP Allowlist.

        Returns the IP allowlist and its enabled or disabled state.

        :rtype: IPAllowlistResponse
        """
        kwargs: Dict[str, Any] = {}
        return self._get_ip_allowlist_endpoint.call_with_http_info(**kwargs)

    def update_ip_allowlist(
        self,
        body: IPAllowlistUpdateRequest,
    ) -> IPAllowlistResponse:
        """Update IP Allowlist.

        Edit the entries in the IP allowlist, and enable or disable it.

        :type body: IPAllowlistUpdateRequest
        :rtype: IPAllowlistResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["body"] = body

        return self._update_ip_allowlist_endpoint.call_with_http_info(**kwargs)
