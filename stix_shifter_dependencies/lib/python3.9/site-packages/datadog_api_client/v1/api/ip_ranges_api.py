# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Any, Dict

from datadog_api_client.api_client import ApiClient, Endpoint as _Endpoint
from datadog_api_client.configuration import Configuration
from datadog_api_client.v1.model.ip_ranges import IPRanges


class IPRangesApi:
    """
    Get a list of IP prefixes belonging to Datadog.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient(Configuration())
        self.api_client = api_client

        self._get_ip_ranges_endpoint = _Endpoint(
            settings={
                "response_type": (IPRanges,),
                "auth": [],
                "endpoint_path": "/",
                "operation_id": "get_ip_ranges",
                "http_method": "GET",
                "version": "v1",
                "servers": [
                    {
                        "url": "https://{subdomain}.{site}",
                        "variables": {
                            "site": {
                                "description": "The regional site for Datadog customers.",
                                "default_value": "datadoghq.com",
                                "enum_values": [
                                    "datadoghq.com",
                                    "us3.datadoghq.com",
                                    "us5.datadoghq.com",
                                    "ap1.datadoghq.com",
                                    "datadoghq.eu",
                                    "ddog-gov.com",
                                ],
                            },
                            "subdomain": {
                                "description": "The subdomain where the API is deployed.",
                                "default_value": "ip-ranges",
                            },
                        },
                    },
                    {
                        "url": "{protocol}://{name}",
                        "variables": {
                            "name": {
                                "description": "Full site DNS name.",
                                "default_value": "ip-ranges.datadoghq.com",
                            },
                            "protocol": {
                                "description": "The protocol for accessing the API.",
                                "default_value": "https",
                            },
                        },
                    },
                    {
                        "url": "https://{subdomain}.datadoghq.com",
                        "variables": {
                            "subdomain": {
                                "description": "The subdomain where the API is deployed.",
                                "default_value": "ip-ranges",
                            },
                        },
                    },
                ],
            },
            params_map={},
            headers_map={
                "accept": ["application/json"],
                "content_type": [],
            },
            api_client=api_client,
        )

    def get_ip_ranges(
        self,
    ) -> IPRanges:
        """List IP Ranges.

        Get information about Datadog IP ranges.

        :rtype: IPRanges
        """
        kwargs: Dict[str, Any] = {}
        return self._get_ip_ranges_endpoint.call_with_http_info(**kwargs)
