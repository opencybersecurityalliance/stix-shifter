# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Any, Dict

from datadog_api_client.api_client import ApiClient, Endpoint as _Endpoint
from datadog_api_client.configuration import Configuration
from datadog_api_client.model_utils import (
    file_type,
)
from datadog_api_client.v2.model.cloud_workload_security_agent_rules_list_response import (
    CloudWorkloadSecurityAgentRulesListResponse,
)
from datadog_api_client.v2.model.cloud_workload_security_agent_rule_response import (
    CloudWorkloadSecurityAgentRuleResponse,
)
from datadog_api_client.v2.model.cloud_workload_security_agent_rule_create_request import (
    CloudWorkloadSecurityAgentRuleCreateRequest,
)
from datadog_api_client.v2.model.cloud_workload_security_agent_rule_update_request import (
    CloudWorkloadSecurityAgentRuleUpdateRequest,
)


class CloudWorkloadSecurityApi:
    """
    Workload activity security rules for generating events using the Datadog security Agent.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient(Configuration())
        self.api_client = api_client

        self._create_cloud_workload_security_agent_rule_endpoint = _Endpoint(
            settings={
                "response_type": (CloudWorkloadSecurityAgentRuleResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v2/security_monitoring/cloud_workload_security/agent_rules",
                "operation_id": "create_cloud_workload_security_agent_rule",
                "http_method": "POST",
                "version": "v2",
                "servers": None,
            },
            params_map={
                "body": {
                    "required": True,
                    "openapi_types": (CloudWorkloadSecurityAgentRuleCreateRequest,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

        self._delete_cloud_workload_security_agent_rule_endpoint = _Endpoint(
            settings={
                "response_type": None,
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v2/security_monitoring/cloud_workload_security/agent_rules/{agent_rule_id}",
                "operation_id": "delete_cloud_workload_security_agent_rule",
                "http_method": "DELETE",
                "version": "v2",
                "servers": None,
            },
            params_map={
                "agent_rule_id": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "agent_rule_id",
                    "location": "path",
                },
            },
            headers_map={
                "accept": ["*/*"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._download_cloud_workload_policy_file_endpoint = _Endpoint(
            settings={
                "response_type": (file_type,),
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v2/security/cloud_workload/policy/download",
                "operation_id": "download_cloud_workload_policy_file",
                "http_method": "GET",
                "version": "v2",
                "servers": None,
            },
            params_map={},
            headers_map={
                "accept": ["application/yaml", "application/json"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._get_cloud_workload_security_agent_rule_endpoint = _Endpoint(
            settings={
                "response_type": (CloudWorkloadSecurityAgentRuleResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v2/security_monitoring/cloud_workload_security/agent_rules/{agent_rule_id}",
                "operation_id": "get_cloud_workload_security_agent_rule",
                "http_method": "GET",
                "version": "v2",
                "servers": None,
            },
            params_map={
                "agent_rule_id": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "agent_rule_id",
                    "location": "path",
                },
            },
            headers_map={
                "accept": ["application/json"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._list_cloud_workload_security_agent_rules_endpoint = _Endpoint(
            settings={
                "response_type": (CloudWorkloadSecurityAgentRulesListResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v2/security_monitoring/cloud_workload_security/agent_rules",
                "operation_id": "list_cloud_workload_security_agent_rules",
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

        self._update_cloud_workload_security_agent_rule_endpoint = _Endpoint(
            settings={
                "response_type": (CloudWorkloadSecurityAgentRuleResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v2/security_monitoring/cloud_workload_security/agent_rules/{agent_rule_id}",
                "operation_id": "update_cloud_workload_security_agent_rule",
                "http_method": "PATCH",
                "version": "v2",
                "servers": None,
            },
            params_map={
                "agent_rule_id": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "agent_rule_id",
                    "location": "path",
                },
                "body": {
                    "required": True,
                    "openapi_types": (CloudWorkloadSecurityAgentRuleUpdateRequest,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

    def create_cloud_workload_security_agent_rule(
        self,
        body: CloudWorkloadSecurityAgentRuleCreateRequest,
    ) -> CloudWorkloadSecurityAgentRuleResponse:
        """Create a Cloud Workload Security Agent rule.

        Create a new Agent rule with the given parameters.

        :param body: The definition of the new Agent rule.
        :type body: CloudWorkloadSecurityAgentRuleCreateRequest
        :rtype: CloudWorkloadSecurityAgentRuleResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["body"] = body

        return self._create_cloud_workload_security_agent_rule_endpoint.call_with_http_info(**kwargs)

    def delete_cloud_workload_security_agent_rule(
        self,
        agent_rule_id: str,
    ) -> None:
        """Delete a Cloud Workload Security Agent rule.

        Delete a specific Agent rule.

        :param agent_rule_id: The ID of the Agent rule.
        :type agent_rule_id: str
        :rtype: None
        """
        kwargs: Dict[str, Any] = {}
        kwargs["agent_rule_id"] = agent_rule_id

        return self._delete_cloud_workload_security_agent_rule_endpoint.call_with_http_info(**kwargs)

    def download_cloud_workload_policy_file(
        self,
    ) -> file_type:
        """Get the latest Cloud Workload Security policy.

        The download endpoint generates a Cloud Workload Security policy file from your currently active
        Cloud Workload Security rules, and downloads them as a .policy file. This file can then be deployed to
        your Agents to update the policy running in your environment.

        :rtype: file_type
        """
        kwargs: Dict[str, Any] = {}
        return self._download_cloud_workload_policy_file_endpoint.call_with_http_info(**kwargs)

    def get_cloud_workload_security_agent_rule(
        self,
        agent_rule_id: str,
    ) -> CloudWorkloadSecurityAgentRuleResponse:
        """Get a Cloud Workload Security Agent rule.

        Get the details of a specific Agent rule.

        :param agent_rule_id: The ID of the Agent rule.
        :type agent_rule_id: str
        :rtype: CloudWorkloadSecurityAgentRuleResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["agent_rule_id"] = agent_rule_id

        return self._get_cloud_workload_security_agent_rule_endpoint.call_with_http_info(**kwargs)

    def list_cloud_workload_security_agent_rules(
        self,
    ) -> CloudWorkloadSecurityAgentRulesListResponse:
        """Get all Cloud Workload Security Agent rules.

        Get the list of Agent rules.

        :rtype: CloudWorkloadSecurityAgentRulesListResponse
        """
        kwargs: Dict[str, Any] = {}
        return self._list_cloud_workload_security_agent_rules_endpoint.call_with_http_info(**kwargs)

    def update_cloud_workload_security_agent_rule(
        self,
        agent_rule_id: str,
        body: CloudWorkloadSecurityAgentRuleUpdateRequest,
    ) -> CloudWorkloadSecurityAgentRuleResponse:
        """Update a Cloud Workload Security Agent rule.

        Update a specific Agent rule.
        Returns the Agent rule object when the request is successful.

        :param agent_rule_id: The ID of the Agent rule.
        :type agent_rule_id: str
        :param body: New definition of the Agent rule.
        :type body: CloudWorkloadSecurityAgentRuleUpdateRequest
        :rtype: CloudWorkloadSecurityAgentRuleResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["agent_rule_id"] = agent_rule_id

        kwargs["body"] = body

        return self._update_cloud_workload_security_agent_rule_endpoint.call_with_http_info(**kwargs)
