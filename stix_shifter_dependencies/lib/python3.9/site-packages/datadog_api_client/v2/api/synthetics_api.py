# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Any, Dict

from datadog_api_client.api_client import ApiClient, Endpoint as _Endpoint
from datadog_api_client.configuration import Configuration
from datadog_api_client.v2.model.on_demand_concurrency_cap_response import OnDemandConcurrencyCapResponse
from datadog_api_client.v2.model.on_demand_concurrency_cap_attributes import OnDemandConcurrencyCapAttributes


class SyntheticsApi:
    """
    Datadog Synthetics uses simulated user requests and browser rendering to help you ensure uptime,
    identify regional issues, and track your application performance. Datadog Synthetics tests come in
    two different flavors, `API tests <https://docs.datadoghq.com/synthetics/api_tests/>`_
    and `browser tests <https://docs.datadoghq.com/synthetics/browser_tests>`_. You can use Datadog’s API to
    manage both test types programmatically.

    For more information about Synthetics, see the `Synthetics overview <https://docs.datadoghq.com/synthetics/>`_.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient(Configuration())
        self.api_client = api_client

        self._get_on_demand_concurrency_cap_endpoint = _Endpoint(
            settings={
                "response_type": (OnDemandConcurrencyCapResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v2/synthetics/settings/on_demand_concurrency_cap",
                "operation_id": "get_on_demand_concurrency_cap",
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

        self._set_on_demand_concurrency_cap_endpoint = _Endpoint(
            settings={
                "response_type": (OnDemandConcurrencyCapResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v2/synthetics/settings/on_demand_concurrency_cap",
                "operation_id": "set_on_demand_concurrency_cap",
                "http_method": "POST",
                "version": "v2",
                "servers": None,
            },
            params_map={
                "body": {
                    "required": True,
                    "openapi_types": (OnDemandConcurrencyCapAttributes,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

    def get_on_demand_concurrency_cap(
        self,
    ) -> OnDemandConcurrencyCapResponse:
        """Get the on-demand concurrency cap.

        Get the on-demand concurrency cap.

        :rtype: OnDemandConcurrencyCapResponse
        """
        kwargs: Dict[str, Any] = {}
        return self._get_on_demand_concurrency_cap_endpoint.call_with_http_info(**kwargs)

    def set_on_demand_concurrency_cap(
        self,
        body: OnDemandConcurrencyCapAttributes,
    ) -> OnDemandConcurrencyCapResponse:
        """Save new value for on-demand concurrency cap.

        Save new value for on-demand concurrency cap.

        :param body: .
        :type body: OnDemandConcurrencyCapAttributes
        :rtype: OnDemandConcurrencyCapResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["body"] = body

        return self._set_on_demand_concurrency_cap_endpoint.call_with_http_info(**kwargs)
