# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Any, Dict

from datadog_api_client.api_client import ApiClient, Endpoint as _Endpoint
from datadog_api_client.configuration import Configuration
from datadog_api_client.v2.model.monitor_config_policy_list_response import MonitorConfigPolicyListResponse
from datadog_api_client.v2.model.monitor_config_policy_response import MonitorConfigPolicyResponse
from datadog_api_client.v2.model.monitor_config_policy_create_request import MonitorConfigPolicyCreateRequest
from datadog_api_client.v2.model.monitor_config_policy_edit_request import MonitorConfigPolicyEditRequest


class MonitorsApi:
    """
    `Monitors <https://docs.datadoghq.com/monitors>`_ allow you to watch a metric or check that you care about and
    notifies your team when a defined threshold has exceeded.

    For more information, see `Creating Monitors <https://docs.datadoghq.com/monitors/create/types/>`_ and
    `Tag Policies <https://docs.datadoghq.com/monitors/settings/>`_.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient(Configuration())
        self.api_client = api_client

        self._create_monitor_config_policy_endpoint = _Endpoint(
            settings={
                "response_type": (MonitorConfigPolicyResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v2/monitor/policy",
                "operation_id": "create_monitor_config_policy",
                "http_method": "POST",
                "version": "v2",
                "servers": None,
            },
            params_map={
                "body": {
                    "required": True,
                    "openapi_types": (MonitorConfigPolicyCreateRequest,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

        self._delete_monitor_config_policy_endpoint = _Endpoint(
            settings={
                "response_type": None,
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v2/monitor/policy/{policy_id}",
                "operation_id": "delete_monitor_config_policy",
                "http_method": "DELETE",
                "version": "v2",
                "servers": None,
            },
            params_map={
                "policy_id": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "policy_id",
                    "location": "path",
                },
            },
            headers_map={
                "accept": ["*/*"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._get_monitor_config_policy_endpoint = _Endpoint(
            settings={
                "response_type": (MonitorConfigPolicyResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v2/monitor/policy/{policy_id}",
                "operation_id": "get_monitor_config_policy",
                "http_method": "GET",
                "version": "v2",
                "servers": None,
            },
            params_map={
                "policy_id": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "policy_id",
                    "location": "path",
                },
            },
            headers_map={
                "accept": ["application/json"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._list_monitor_config_policies_endpoint = _Endpoint(
            settings={
                "response_type": (MonitorConfigPolicyListResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v2/monitor/policy",
                "operation_id": "list_monitor_config_policies",
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

        self._update_monitor_config_policy_endpoint = _Endpoint(
            settings={
                "response_type": (MonitorConfigPolicyResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v2/monitor/policy/{policy_id}",
                "operation_id": "update_monitor_config_policy",
                "http_method": "PATCH",
                "version": "v2",
                "servers": None,
            },
            params_map={
                "policy_id": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "policy_id",
                    "location": "path",
                },
                "body": {
                    "required": True,
                    "openapi_types": (MonitorConfigPolicyEditRequest,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

    def create_monitor_config_policy(
        self,
        body: MonitorConfigPolicyCreateRequest,
    ) -> MonitorConfigPolicyResponse:
        """Create a monitor configuration policy.

        Create a monitor configuration policy.

        :param body: Create a monitor configuration policy request body.
        :type body: MonitorConfigPolicyCreateRequest
        :rtype: MonitorConfigPolicyResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["body"] = body

        return self._create_monitor_config_policy_endpoint.call_with_http_info(**kwargs)

    def delete_monitor_config_policy(
        self,
        policy_id: str,
    ) -> None:
        """Delete a monitor configuration policy.

        Delete a monitor configuration policy.

        :param policy_id: ID of the monitor configuration policy.
        :type policy_id: str
        :rtype: None
        """
        kwargs: Dict[str, Any] = {}
        kwargs["policy_id"] = policy_id

        return self._delete_monitor_config_policy_endpoint.call_with_http_info(**kwargs)

    def get_monitor_config_policy(
        self,
        policy_id: str,
    ) -> MonitorConfigPolicyResponse:
        """Get a monitor configuration policy.

        Get a monitor configuration policy by ``policy_id``.

        :param policy_id: ID of the monitor configuration policy.
        :type policy_id: str
        :rtype: MonitorConfigPolicyResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["policy_id"] = policy_id

        return self._get_monitor_config_policy_endpoint.call_with_http_info(**kwargs)

    def list_monitor_config_policies(
        self,
    ) -> MonitorConfigPolicyListResponse:
        """Get all monitor configuration policies.

        Get all monitor configuration policies.

        :rtype: MonitorConfigPolicyListResponse
        """
        kwargs: Dict[str, Any] = {}
        return self._list_monitor_config_policies_endpoint.call_with_http_info(**kwargs)

    def update_monitor_config_policy(
        self,
        policy_id: str,
        body: MonitorConfigPolicyEditRequest,
    ) -> MonitorConfigPolicyResponse:
        """Edit a monitor configuration policy.

        Edit a monitor configuration policy.

        :param policy_id: ID of the monitor configuration policy.
        :type policy_id: str
        :param body: Description of the update.
        :type body: MonitorConfigPolicyEditRequest
        :rtype: MonitorConfigPolicyResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["policy_id"] = policy_id

        kwargs["body"] = body

        return self._update_monitor_config_policy_endpoint.call_with_http_info(**kwargs)
