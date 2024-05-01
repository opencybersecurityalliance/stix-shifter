# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Any, Dict

from datadog_api_client.api_client import ApiClient, Endpoint as _Endpoint
from datadog_api_client.configuration import Configuration
from datadog_api_client.v2.model.sensitive_data_scanner_get_config_response import SensitiveDataScannerGetConfigResponse
from datadog_api_client.v2.model.sensitive_data_scanner_reorder_groups_response import (
    SensitiveDataScannerReorderGroupsResponse,
)
from datadog_api_client.v2.model.sensitive_data_scanner_config_request import SensitiveDataScannerConfigRequest
from datadog_api_client.v2.model.sensitive_data_scanner_create_group_response import (
    SensitiveDataScannerCreateGroupResponse,
)
from datadog_api_client.v2.model.sensitive_data_scanner_group_create_request import (
    SensitiveDataScannerGroupCreateRequest,
)
from datadog_api_client.v2.model.sensitive_data_scanner_group_delete_response import (
    SensitiveDataScannerGroupDeleteResponse,
)
from datadog_api_client.v2.model.sensitive_data_scanner_group_delete_request import (
    SensitiveDataScannerGroupDeleteRequest,
)
from datadog_api_client.v2.model.sensitive_data_scanner_group_update_response import (
    SensitiveDataScannerGroupUpdateResponse,
)
from datadog_api_client.v2.model.sensitive_data_scanner_group_update_request import (
    SensitiveDataScannerGroupUpdateRequest,
)
from datadog_api_client.v2.model.sensitive_data_scanner_create_rule_response import (
    SensitiveDataScannerCreateRuleResponse,
)
from datadog_api_client.v2.model.sensitive_data_scanner_rule_create_request import SensitiveDataScannerRuleCreateRequest
from datadog_api_client.v2.model.sensitive_data_scanner_rule_delete_response import (
    SensitiveDataScannerRuleDeleteResponse,
)
from datadog_api_client.v2.model.sensitive_data_scanner_rule_delete_request import SensitiveDataScannerRuleDeleteRequest
from datadog_api_client.v2.model.sensitive_data_scanner_rule_update_response import (
    SensitiveDataScannerRuleUpdateResponse,
)
from datadog_api_client.v2.model.sensitive_data_scanner_rule_update_request import SensitiveDataScannerRuleUpdateRequest
from datadog_api_client.v2.model.sensitive_data_scanner_standard_patterns_response_data import (
    SensitiveDataScannerStandardPatternsResponseData,
)


class SensitiveDataScannerApi:
    """
    Create, update, delete, and retrieve sensitive data scanner groups and rules.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient(Configuration())
        self.api_client = api_client

        self._create_scanning_group_endpoint = _Endpoint(
            settings={
                "response_type": (SensitiveDataScannerCreateGroupResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v2/sensitive-data-scanner/config/groups",
                "operation_id": "create_scanning_group",
                "http_method": "POST",
                "version": "v2",
                "servers": None,
            },
            params_map={
                "body": {
                    "required": True,
                    "openapi_types": (SensitiveDataScannerGroupCreateRequest,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

        self._create_scanning_rule_endpoint = _Endpoint(
            settings={
                "response_type": (SensitiveDataScannerCreateRuleResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v2/sensitive-data-scanner/config/rules",
                "operation_id": "create_scanning_rule",
                "http_method": "POST",
                "version": "v2",
                "servers": None,
            },
            params_map={
                "body": {
                    "required": True,
                    "openapi_types": (SensitiveDataScannerRuleCreateRequest,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

        self._delete_scanning_group_endpoint = _Endpoint(
            settings={
                "response_type": (SensitiveDataScannerGroupDeleteResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v2/sensitive-data-scanner/config/groups/{group_id}",
                "operation_id": "delete_scanning_group",
                "http_method": "DELETE",
                "version": "v2",
                "servers": None,
            },
            params_map={
                "group_id": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "group_id",
                    "location": "path",
                },
                "body": {
                    "required": True,
                    "openapi_types": (SensitiveDataScannerGroupDeleteRequest,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

        self._delete_scanning_rule_endpoint = _Endpoint(
            settings={
                "response_type": (SensitiveDataScannerRuleDeleteResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v2/sensitive-data-scanner/config/rules/{rule_id}",
                "operation_id": "delete_scanning_rule",
                "http_method": "DELETE",
                "version": "v2",
                "servers": None,
            },
            params_map={
                "rule_id": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "rule_id",
                    "location": "path",
                },
                "body": {
                    "required": True,
                    "openapi_types": (SensitiveDataScannerRuleDeleteRequest,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

        self._list_scanning_groups_endpoint = _Endpoint(
            settings={
                "response_type": (SensitiveDataScannerGetConfigResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v2/sensitive-data-scanner/config",
                "operation_id": "list_scanning_groups",
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

        self._list_standard_patterns_endpoint = _Endpoint(
            settings={
                "response_type": (SensitiveDataScannerStandardPatternsResponseData,),
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v2/sensitive-data-scanner/config/standard-patterns",
                "operation_id": "list_standard_patterns",
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

        self._reorder_scanning_groups_endpoint = _Endpoint(
            settings={
                "response_type": (SensitiveDataScannerReorderGroupsResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v2/sensitive-data-scanner/config",
                "operation_id": "reorder_scanning_groups",
                "http_method": "PATCH",
                "version": "v2",
                "servers": None,
            },
            params_map={
                "body": {
                    "required": True,
                    "openapi_types": (SensitiveDataScannerConfigRequest,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

        self._update_scanning_group_endpoint = _Endpoint(
            settings={
                "response_type": (SensitiveDataScannerGroupUpdateResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v2/sensitive-data-scanner/config/groups/{group_id}",
                "operation_id": "update_scanning_group",
                "http_method": "PATCH",
                "version": "v2",
                "servers": None,
            },
            params_map={
                "group_id": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "group_id",
                    "location": "path",
                },
                "body": {
                    "required": True,
                    "openapi_types": (SensitiveDataScannerGroupUpdateRequest,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

        self._update_scanning_rule_endpoint = _Endpoint(
            settings={
                "response_type": (SensitiveDataScannerRuleUpdateResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v2/sensitive-data-scanner/config/rules/{rule_id}",
                "operation_id": "update_scanning_rule",
                "http_method": "PATCH",
                "version": "v2",
                "servers": None,
            },
            params_map={
                "rule_id": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "rule_id",
                    "location": "path",
                },
                "body": {
                    "required": True,
                    "openapi_types": (SensitiveDataScannerRuleUpdateRequest,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

    def create_scanning_group(
        self,
        body: SensitiveDataScannerGroupCreateRequest,
    ) -> SensitiveDataScannerCreateGroupResponse:
        """Create Scanning Group.

        Create a scanning group.
        The request MAY include a configuration relationship.
        A rules relationship can be omitted entirely, but if it is included it MUST be
        null or an empty array (rules cannot be created at the same time).
        The new group will be ordered last within the configuration.

        :type body: SensitiveDataScannerGroupCreateRequest
        :rtype: SensitiveDataScannerCreateGroupResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["body"] = body

        return self._create_scanning_group_endpoint.call_with_http_info(**kwargs)

    def create_scanning_rule(
        self,
        body: SensitiveDataScannerRuleCreateRequest,
    ) -> SensitiveDataScannerCreateRuleResponse:
        """Create Scanning Rule.

        Create a scanning rule in a sensitive data scanner group, ordered last.
        The posted rule MUST include a group relationship.
        It MUST include either a standard_pattern relationship or a regex attribute, but not both.
        If included_attributes is empty or missing, we will scan all attributes except
        excluded_attributes. If both are missing, we will scan the whole event.

        :type body: SensitiveDataScannerRuleCreateRequest
        :rtype: SensitiveDataScannerCreateRuleResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["body"] = body

        return self._create_scanning_rule_endpoint.call_with_http_info(**kwargs)

    def delete_scanning_group(
        self,
        group_id: str,
        body: SensitiveDataScannerGroupDeleteRequest,
    ) -> SensitiveDataScannerGroupDeleteResponse:
        """Delete Scanning Group.

        Delete a given group.

        :param group_id: The ID of a group of rules.
        :type group_id: str
        :type body: SensitiveDataScannerGroupDeleteRequest
        :rtype: SensitiveDataScannerGroupDeleteResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["group_id"] = group_id

        kwargs["body"] = body

        return self._delete_scanning_group_endpoint.call_with_http_info(**kwargs)

    def delete_scanning_rule(
        self,
        rule_id: str,
        body: SensitiveDataScannerRuleDeleteRequest,
    ) -> SensitiveDataScannerRuleDeleteResponse:
        """Delete Scanning Rule.

        Delete a given rule.

        :param rule_id: The ID of the rule.
        :type rule_id: str
        :type body: SensitiveDataScannerRuleDeleteRequest
        :rtype: SensitiveDataScannerRuleDeleteResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["rule_id"] = rule_id

        kwargs["body"] = body

        return self._delete_scanning_rule_endpoint.call_with_http_info(**kwargs)

    def list_scanning_groups(
        self,
    ) -> SensitiveDataScannerGetConfigResponse:
        """List Scanning Groups.

        List all the Scanning groups in your organization.

        :rtype: SensitiveDataScannerGetConfigResponse
        """
        kwargs: Dict[str, Any] = {}
        return self._list_scanning_groups_endpoint.call_with_http_info(**kwargs)

    def list_standard_patterns(
        self,
    ) -> SensitiveDataScannerStandardPatternsResponseData:
        """List standard patterns.

        Returns all standard patterns.

        :rtype: SensitiveDataScannerStandardPatternsResponseData
        """
        kwargs: Dict[str, Any] = {}
        return self._list_standard_patterns_endpoint.call_with_http_info(**kwargs)

    def reorder_scanning_groups(
        self,
        body: SensitiveDataScannerConfigRequest,
    ) -> SensitiveDataScannerReorderGroupsResponse:
        """Reorder Groups.

        Reorder the list of groups.

        :type body: SensitiveDataScannerConfigRequest
        :rtype: SensitiveDataScannerReorderGroupsResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["body"] = body

        return self._reorder_scanning_groups_endpoint.call_with_http_info(**kwargs)

    def update_scanning_group(
        self,
        group_id: str,
        body: SensitiveDataScannerGroupUpdateRequest,
    ) -> SensitiveDataScannerGroupUpdateResponse:
        """Update Scanning Group.

        Update a group, including the order of the rules.
        Rules within the group are reordered by including a rules relationship. If the rules
        relationship is present, its data section MUST contain linkages for all of the rules
        currently in the group, and MUST NOT contain any others.

        :param group_id: The ID of a group of rules.
        :type group_id: str
        :type body: SensitiveDataScannerGroupUpdateRequest
        :rtype: SensitiveDataScannerGroupUpdateResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["group_id"] = group_id

        kwargs["body"] = body

        return self._update_scanning_group_endpoint.call_with_http_info(**kwargs)

    def update_scanning_rule(
        self,
        rule_id: str,
        body: SensitiveDataScannerRuleUpdateRequest,
    ) -> SensitiveDataScannerRuleUpdateResponse:
        """Update Scanning Rule.

        Update a scanning rule.
        The request body MUST NOT include a standard_pattern relationship, as that relationship
        is non-editable. Trying to edit the regex attribute of a rule with a standard_pattern
        relationship will also result in an error.

        :param rule_id: The ID of the rule.
        :type rule_id: str
        :type body: SensitiveDataScannerRuleUpdateRequest
        :rtype: SensitiveDataScannerRuleUpdateResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["rule_id"] = rule_id

        kwargs["body"] = body

        return self._update_scanning_rule_endpoint.call_with_http_info(**kwargs)
