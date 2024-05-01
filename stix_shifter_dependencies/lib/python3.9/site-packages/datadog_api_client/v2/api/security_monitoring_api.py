# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

import collections
from typing import Any, Dict, Union

from datadog_api_client.api_client import ApiClient, Endpoint as _Endpoint
from datadog_api_client.configuration import Configuration
from datadog_api_client.model_utils import (
    datetime,
    set_attribute_from_path,
    get_attribute_from_path,
    UnsetType,
    unset,
)
from datadog_api_client.v2.model.security_filters_response import SecurityFiltersResponse
from datadog_api_client.v2.model.security_filter_response import SecurityFilterResponse
from datadog_api_client.v2.model.security_filter_create_request import SecurityFilterCreateRequest
from datadog_api_client.v2.model.security_filter_update_request import SecurityFilterUpdateRequest
from datadog_api_client.v2.model.security_monitoring_list_rules_response import SecurityMonitoringListRulesResponse
from datadog_api_client.v2.model.security_monitoring_rule_response import SecurityMonitoringRuleResponse
from datadog_api_client.v2.model.security_monitoring_rule_create_payload import SecurityMonitoringRuleCreatePayload
from datadog_api_client.v2.model.security_monitoring_standard_rule_create_payload import (
    SecurityMonitoringStandardRuleCreatePayload,
)
from datadog_api_client.v2.model.security_monitoring_signal_rule_create_payload import (
    SecurityMonitoringSignalRuleCreatePayload,
)
from datadog_api_client.v2.model.cloud_configuration_rule_create_payload import CloudConfigurationRuleCreatePayload
from datadog_api_client.v2.model.security_monitoring_rule_update_payload import SecurityMonitoringRuleUpdatePayload
from datadog_api_client.v2.model.security_monitoring_signals_list_response import SecurityMonitoringSignalsListResponse
from datadog_api_client.v2.model.security_monitoring_signals_sort import SecurityMonitoringSignalsSort
from datadog_api_client.v2.model.security_monitoring_signal import SecurityMonitoringSignal
from datadog_api_client.v2.model.security_monitoring_signal_list_request import SecurityMonitoringSignalListRequest
from datadog_api_client.v2.model.security_monitoring_signal_triage_update_response import (
    SecurityMonitoringSignalTriageUpdateResponse,
)
from datadog_api_client.v2.model.security_monitoring_signal_assignee_update_request import (
    SecurityMonitoringSignalAssigneeUpdateRequest,
)
from datadog_api_client.v2.model.security_monitoring_signal_incidents_update_request import (
    SecurityMonitoringSignalIncidentsUpdateRequest,
)
from datadog_api_client.v2.model.security_monitoring_signal_state_update_request import (
    SecurityMonitoringSignalStateUpdateRequest,
)


class SecurityMonitoringApi:
    """
    Detection rules for generating signals and listing of generated
    signals.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient(Configuration())
        self.api_client = api_client

        self._create_security_filter_endpoint = _Endpoint(
            settings={
                "response_type": (SecurityFilterResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v2/security_monitoring/configuration/security_filters",
                "operation_id": "create_security_filter",
                "http_method": "POST",
                "version": "v2",
                "servers": None,
            },
            params_map={
                "body": {
                    "required": True,
                    "openapi_types": (SecurityFilterCreateRequest,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

        self._create_security_monitoring_rule_endpoint = _Endpoint(
            settings={
                "response_type": (SecurityMonitoringRuleResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v2/security_monitoring/rules",
                "operation_id": "create_security_monitoring_rule",
                "http_method": "POST",
                "version": "v2",
                "servers": None,
            },
            params_map={
                "body": {
                    "required": True,
                    "openapi_types": (SecurityMonitoringRuleCreatePayload,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

        self._delete_security_filter_endpoint = _Endpoint(
            settings={
                "response_type": None,
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v2/security_monitoring/configuration/security_filters/{security_filter_id}",
                "operation_id": "delete_security_filter",
                "http_method": "DELETE",
                "version": "v2",
                "servers": None,
            },
            params_map={
                "security_filter_id": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "security_filter_id",
                    "location": "path",
                },
            },
            headers_map={
                "accept": ["*/*"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._delete_security_monitoring_rule_endpoint = _Endpoint(
            settings={
                "response_type": None,
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v2/security_monitoring/rules/{rule_id}",
                "operation_id": "delete_security_monitoring_rule",
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
            },
            headers_map={
                "accept": ["*/*"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._edit_security_monitoring_signal_assignee_endpoint = _Endpoint(
            settings={
                "response_type": (SecurityMonitoringSignalTriageUpdateResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v2/security_monitoring/signals/{signal_id}/assignee",
                "operation_id": "edit_security_monitoring_signal_assignee",
                "http_method": "PATCH",
                "version": "v2",
                "servers": None,
            },
            params_map={
                "signal_id": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "signal_id",
                    "location": "path",
                },
                "body": {
                    "required": True,
                    "openapi_types": (SecurityMonitoringSignalAssigneeUpdateRequest,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

        self._edit_security_monitoring_signal_incidents_endpoint = _Endpoint(
            settings={
                "response_type": (SecurityMonitoringSignalTriageUpdateResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v2/security_monitoring/signals/{signal_id}/incidents",
                "operation_id": "edit_security_monitoring_signal_incidents",
                "http_method": "PATCH",
                "version": "v2",
                "servers": None,
            },
            params_map={
                "signal_id": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "signal_id",
                    "location": "path",
                },
                "body": {
                    "required": True,
                    "openapi_types": (SecurityMonitoringSignalIncidentsUpdateRequest,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

        self._edit_security_monitoring_signal_state_endpoint = _Endpoint(
            settings={
                "response_type": (SecurityMonitoringSignalTriageUpdateResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v2/security_monitoring/signals/{signal_id}/state",
                "operation_id": "edit_security_monitoring_signal_state",
                "http_method": "PATCH",
                "version": "v2",
                "servers": None,
            },
            params_map={
                "signal_id": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "signal_id",
                    "location": "path",
                },
                "body": {
                    "required": True,
                    "openapi_types": (SecurityMonitoringSignalStateUpdateRequest,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

        self._get_security_filter_endpoint = _Endpoint(
            settings={
                "response_type": (SecurityFilterResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v2/security_monitoring/configuration/security_filters/{security_filter_id}",
                "operation_id": "get_security_filter",
                "http_method": "GET",
                "version": "v2",
                "servers": None,
            },
            params_map={
                "security_filter_id": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "security_filter_id",
                    "location": "path",
                },
            },
            headers_map={
                "accept": ["application/json"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._get_security_monitoring_rule_endpoint = _Endpoint(
            settings={
                "response_type": (SecurityMonitoringRuleResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v2/security_monitoring/rules/{rule_id}",
                "operation_id": "get_security_monitoring_rule",
                "http_method": "GET",
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
            },
            headers_map={
                "accept": ["application/json"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._get_security_monitoring_signal_endpoint = _Endpoint(
            settings={
                "response_type": (SecurityMonitoringSignal,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v2/security_monitoring/signals/{signal_id}",
                "operation_id": "get_security_monitoring_signal",
                "http_method": "GET",
                "version": "v2",
                "servers": None,
            },
            params_map={
                "signal_id": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "signal_id",
                    "location": "path",
                },
            },
            headers_map={
                "accept": ["application/json"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._list_security_filters_endpoint = _Endpoint(
            settings={
                "response_type": (SecurityFiltersResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v2/security_monitoring/configuration/security_filters",
                "operation_id": "list_security_filters",
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

        self._list_security_monitoring_rules_endpoint = _Endpoint(
            settings={
                "response_type": (SecurityMonitoringListRulesResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v2/security_monitoring/rules",
                "operation_id": "list_security_monitoring_rules",
                "http_method": "GET",
                "version": "v2",
                "servers": None,
            },
            params_map={
                "page_size": {
                    "openapi_types": (int,),
                    "attribute": "page[size]",
                    "location": "query",
                },
                "page_number": {
                    "openapi_types": (int,),
                    "attribute": "page[number]",
                    "location": "query",
                },
            },
            headers_map={
                "accept": ["application/json"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._list_security_monitoring_signals_endpoint = _Endpoint(
            settings={
                "response_type": (SecurityMonitoringSignalsListResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v2/security_monitoring/signals",
                "operation_id": "list_security_monitoring_signals",
                "http_method": "GET",
                "version": "v2",
                "servers": None,
            },
            params_map={
                "filter_query": {
                    "openapi_types": (str,),
                    "attribute": "filter[query]",
                    "location": "query",
                },
                "filter_from": {
                    "openapi_types": (datetime,),
                    "attribute": "filter[from]",
                    "location": "query",
                },
                "filter_to": {
                    "openapi_types": (datetime,),
                    "attribute": "filter[to]",
                    "location": "query",
                },
                "sort": {
                    "openapi_types": (SecurityMonitoringSignalsSort,),
                    "attribute": "sort",
                    "location": "query",
                },
                "page_cursor": {
                    "openapi_types": (str,),
                    "attribute": "page[cursor]",
                    "location": "query",
                },
                "page_limit": {
                    "validation": {
                        "inclusive_maximum": 1000,
                    },
                    "openapi_types": (int,),
                    "attribute": "page[limit]",
                    "location": "query",
                },
            },
            headers_map={
                "accept": ["application/json"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._search_security_monitoring_signals_endpoint = _Endpoint(
            settings={
                "response_type": (SecurityMonitoringSignalsListResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v2/security_monitoring/signals/search",
                "operation_id": "search_security_monitoring_signals",
                "http_method": "POST",
                "version": "v2",
                "servers": None,
            },
            params_map={
                "body": {
                    "openapi_types": (SecurityMonitoringSignalListRequest,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

        self._update_security_filter_endpoint = _Endpoint(
            settings={
                "response_type": (SecurityFilterResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v2/security_monitoring/configuration/security_filters/{security_filter_id}",
                "operation_id": "update_security_filter",
                "http_method": "PATCH",
                "version": "v2",
                "servers": None,
            },
            params_map={
                "security_filter_id": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "security_filter_id",
                    "location": "path",
                },
                "body": {
                    "required": True,
                    "openapi_types": (SecurityFilterUpdateRequest,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

        self._update_security_monitoring_rule_endpoint = _Endpoint(
            settings={
                "response_type": (SecurityMonitoringRuleResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v2/security_monitoring/rules/{rule_id}",
                "operation_id": "update_security_monitoring_rule",
                "http_method": "PUT",
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
                    "openapi_types": (SecurityMonitoringRuleUpdatePayload,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

    def create_security_filter(
        self,
        body: SecurityFilterCreateRequest,
    ) -> SecurityFilterResponse:
        """Create a security filter.

        Create a security filter.

        See the `security filter guide <https://docs.datadoghq.com/security_platform/guide/how-to-setup-security-filters-using-security-monitoring-api/>`_
        for more examples.

        :param body: The definition of the new security filter.
        :type body: SecurityFilterCreateRequest
        :rtype: SecurityFilterResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["body"] = body

        return self._create_security_filter_endpoint.call_with_http_info(**kwargs)

    def create_security_monitoring_rule(
        self,
        body: Union[
            SecurityMonitoringRuleCreatePayload,
            SecurityMonitoringStandardRuleCreatePayload,
            SecurityMonitoringSignalRuleCreatePayload,
            CloudConfigurationRuleCreatePayload,
        ],
    ) -> SecurityMonitoringRuleResponse:
        """Create a detection rule.

        Create a detection rule.

        :type body: SecurityMonitoringRuleCreatePayload
        :rtype: SecurityMonitoringRuleResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["body"] = body

        return self._create_security_monitoring_rule_endpoint.call_with_http_info(**kwargs)

    def delete_security_filter(
        self,
        security_filter_id: str,
    ) -> None:
        """Delete a security filter.

        Delete a specific security filter.

        :param security_filter_id: The ID of the security filter.
        :type security_filter_id: str
        :rtype: None
        """
        kwargs: Dict[str, Any] = {}
        kwargs["security_filter_id"] = security_filter_id

        return self._delete_security_filter_endpoint.call_with_http_info(**kwargs)

    def delete_security_monitoring_rule(
        self,
        rule_id: str,
    ) -> None:
        """Delete an existing rule.

        Delete an existing rule. Default rules cannot be deleted.

        :param rule_id: The ID of the rule.
        :type rule_id: str
        :rtype: None
        """
        kwargs: Dict[str, Any] = {}
        kwargs["rule_id"] = rule_id

        return self._delete_security_monitoring_rule_endpoint.call_with_http_info(**kwargs)

    def edit_security_monitoring_signal_assignee(
        self,
        signal_id: str,
        body: SecurityMonitoringSignalAssigneeUpdateRequest,
    ) -> SecurityMonitoringSignalTriageUpdateResponse:
        """Modify the triage assignee of a security signal.

        Modify the triage assignee of a security signal.

        :param signal_id: The ID of the signal.
        :type signal_id: str
        :param body: Attributes describing the signal update.
        :type body: SecurityMonitoringSignalAssigneeUpdateRequest
        :rtype: SecurityMonitoringSignalTriageUpdateResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["signal_id"] = signal_id

        kwargs["body"] = body

        return self._edit_security_monitoring_signal_assignee_endpoint.call_with_http_info(**kwargs)

    def edit_security_monitoring_signal_incidents(
        self,
        signal_id: str,
        body: SecurityMonitoringSignalIncidentsUpdateRequest,
    ) -> SecurityMonitoringSignalTriageUpdateResponse:
        """Change the related incidents of a security signal.

        Change the related incidents for a security signal.

        :param signal_id: The ID of the signal.
        :type signal_id: str
        :param body: Attributes describing the signal update.
        :type body: SecurityMonitoringSignalIncidentsUpdateRequest
        :rtype: SecurityMonitoringSignalTriageUpdateResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["signal_id"] = signal_id

        kwargs["body"] = body

        return self._edit_security_monitoring_signal_incidents_endpoint.call_with_http_info(**kwargs)

    def edit_security_monitoring_signal_state(
        self,
        signal_id: str,
        body: SecurityMonitoringSignalStateUpdateRequest,
    ) -> SecurityMonitoringSignalTriageUpdateResponse:
        """Change the triage state of a security signal.

        Change the triage state of a security signal.

        :param signal_id: The ID of the signal.
        :type signal_id: str
        :param body: Attributes describing the signal update.
        :type body: SecurityMonitoringSignalStateUpdateRequest
        :rtype: SecurityMonitoringSignalTriageUpdateResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["signal_id"] = signal_id

        kwargs["body"] = body

        return self._edit_security_monitoring_signal_state_endpoint.call_with_http_info(**kwargs)

    def get_security_filter(
        self,
        security_filter_id: str,
    ) -> SecurityFilterResponse:
        """Get a security filter.

        Get the details of a specific security filter.

        See the `security filter guide <https://docs.datadoghq.com/security_platform/guide/how-to-setup-security-filters-using-security-monitoring-api/>`_
        for more examples.

        :param security_filter_id: The ID of the security filter.
        :type security_filter_id: str
        :rtype: SecurityFilterResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["security_filter_id"] = security_filter_id

        return self._get_security_filter_endpoint.call_with_http_info(**kwargs)

    def get_security_monitoring_rule(
        self,
        rule_id: str,
    ) -> SecurityMonitoringRuleResponse:
        """Get a rule's details.

        Get a rule's details.

        :param rule_id: The ID of the rule.
        :type rule_id: str
        :rtype: SecurityMonitoringRuleResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["rule_id"] = rule_id

        return self._get_security_monitoring_rule_endpoint.call_with_http_info(**kwargs)

    def get_security_monitoring_signal(
        self,
        signal_id: str,
    ) -> SecurityMonitoringSignal:
        """Get a signal's details.

        Get a signal's details.

        :param signal_id: The ID of the signal.
        :type signal_id: str
        :rtype: SecurityMonitoringSignal
        """
        kwargs: Dict[str, Any] = {}
        kwargs["signal_id"] = signal_id

        return self._get_security_monitoring_signal_endpoint.call_with_http_info(**kwargs)

    def list_security_filters(
        self,
    ) -> SecurityFiltersResponse:
        """Get all security filters.

        Get the list of configured security filters with their definitions.

        :rtype: SecurityFiltersResponse
        """
        kwargs: Dict[str, Any] = {}
        return self._list_security_filters_endpoint.call_with_http_info(**kwargs)

    def list_security_monitoring_rules(
        self,
        *,
        page_size: Union[int, UnsetType] = unset,
        page_number: Union[int, UnsetType] = unset,
    ) -> SecurityMonitoringListRulesResponse:
        """List rules.

        List rules.

        :param page_size: Size for a given page. The maximum allowed value is 5000.
        :type page_size: int, optional
        :param page_number: Specific page number to return.
        :type page_number: int, optional
        :rtype: SecurityMonitoringListRulesResponse
        """
        kwargs: Dict[str, Any] = {}
        if page_size is not unset:
            kwargs["page_size"] = page_size

        if page_number is not unset:
            kwargs["page_number"] = page_number

        return self._list_security_monitoring_rules_endpoint.call_with_http_info(**kwargs)

    def list_security_monitoring_signals(
        self,
        *,
        filter_query: Union[str, UnsetType] = unset,
        filter_from: Union[datetime, UnsetType] = unset,
        filter_to: Union[datetime, UnsetType] = unset,
        sort: Union[SecurityMonitoringSignalsSort, UnsetType] = unset,
        page_cursor: Union[str, UnsetType] = unset,
        page_limit: Union[int, UnsetType] = unset,
    ) -> SecurityMonitoringSignalsListResponse:
        """Get a quick list of security signals.

        The list endpoint returns security signals that match a search query.
        Both this endpoint and the POST endpoint can be used interchangeably when listing
        security signals.

        :param filter_query: The search query for security signals.
        :type filter_query: str, optional
        :param filter_from: The minimum timestamp for requested security signals.
        :type filter_from: datetime, optional
        :param filter_to: The maximum timestamp for requested security signals.
        :type filter_to: datetime, optional
        :param sort: The order of the security signals in results.
        :type sort: SecurityMonitoringSignalsSort, optional
        :param page_cursor: A list of results using the cursor provided in the previous query.
        :type page_cursor: str, optional
        :param page_limit: The maximum number of security signals in the response.
        :type page_limit: int, optional
        :rtype: SecurityMonitoringSignalsListResponse
        """
        kwargs: Dict[str, Any] = {}
        if filter_query is not unset:
            kwargs["filter_query"] = filter_query

        if filter_from is not unset:
            kwargs["filter_from"] = filter_from

        if filter_to is not unset:
            kwargs["filter_to"] = filter_to

        if sort is not unset:
            kwargs["sort"] = sort

        if page_cursor is not unset:
            kwargs["page_cursor"] = page_cursor

        if page_limit is not unset:
            kwargs["page_limit"] = page_limit

        return self._list_security_monitoring_signals_endpoint.call_with_http_info(**kwargs)

    def list_security_monitoring_signals_with_pagination(
        self,
        *,
        filter_query: Union[str, UnsetType] = unset,
        filter_from: Union[datetime, UnsetType] = unset,
        filter_to: Union[datetime, UnsetType] = unset,
        sort: Union[SecurityMonitoringSignalsSort, UnsetType] = unset,
        page_cursor: Union[str, UnsetType] = unset,
        page_limit: Union[int, UnsetType] = unset,
    ) -> collections.abc.Iterable[SecurityMonitoringSignal]:
        """Get a quick list of security signals.

        Provide a paginated version of :meth:`list_security_monitoring_signals`, returning all items.

        :param filter_query: The search query for security signals.
        :type filter_query: str, optional
        :param filter_from: The minimum timestamp for requested security signals.
        :type filter_from: datetime, optional
        :param filter_to: The maximum timestamp for requested security signals.
        :type filter_to: datetime, optional
        :param sort: The order of the security signals in results.
        :type sort: SecurityMonitoringSignalsSort, optional
        :param page_cursor: A list of results using the cursor provided in the previous query.
        :type page_cursor: str, optional
        :param page_limit: The maximum number of security signals in the response.
        :type page_limit: int, optional

        :return: A generator of paginated results.
        :rtype: collections.abc.Iterable[SecurityMonitoringSignal]
        """
        kwargs: Dict[str, Any] = {}
        if filter_query is not unset:
            kwargs["filter_query"] = filter_query

        if filter_from is not unset:
            kwargs["filter_from"] = filter_from

        if filter_to is not unset:
            kwargs["filter_to"] = filter_to

        if sort is not unset:
            kwargs["sort"] = sort

        if page_cursor is not unset:
            kwargs["page_cursor"] = page_cursor

        if page_limit is not unset:
            kwargs["page_limit"] = page_limit

        local_page_size = get_attribute_from_path(kwargs, "page_limit", 10)
        endpoint = self._list_security_monitoring_signals_endpoint
        set_attribute_from_path(kwargs, "page_limit", local_page_size, endpoint.params_map)
        while True:
            response = endpoint.call_with_http_info(**kwargs)
            for item in get_attribute_from_path(response, "data"):
                yield item
            if len(get_attribute_from_path(response, "data")) < local_page_size:
                break
            set_attribute_from_path(
                kwargs, "page_cursor", get_attribute_from_path(response, "meta.page.after"), endpoint.params_map
            )

    def search_security_monitoring_signals(
        self,
        *,
        body: Union[SecurityMonitoringSignalListRequest, UnsetType] = unset,
    ) -> SecurityMonitoringSignalsListResponse:
        """Get a list of security signals.

        Returns security signals that match a search query.
        Both this endpoint and the GET endpoint can be used interchangeably for listing
        security signals.

        :type body: SecurityMonitoringSignalListRequest, optional
        :rtype: SecurityMonitoringSignalsListResponse
        """
        kwargs: Dict[str, Any] = {}
        if body is not unset:
            kwargs["body"] = body

        return self._search_security_monitoring_signals_endpoint.call_with_http_info(**kwargs)

    def search_security_monitoring_signals_with_pagination(
        self,
        *,
        body: Union[SecurityMonitoringSignalListRequest, UnsetType] = unset,
    ) -> collections.abc.Iterable[SecurityMonitoringSignal]:
        """Get a list of security signals.

        Provide a paginated version of :meth:`search_security_monitoring_signals`, returning all items.

        :type body: SecurityMonitoringSignalListRequest, optional

        :return: A generator of paginated results.
        :rtype: collections.abc.Iterable[SecurityMonitoringSignal]
        """
        kwargs: Dict[str, Any] = {}
        if body is not unset:
            kwargs["body"] = body

        local_page_size = get_attribute_from_path(kwargs, "body.page.limit", 10)
        endpoint = self._search_security_monitoring_signals_endpoint
        set_attribute_from_path(kwargs, "body.page.limit", local_page_size, endpoint.params_map)
        while True:
            response = endpoint.call_with_http_info(**kwargs)
            for item in get_attribute_from_path(response, "data"):
                yield item
            if len(get_attribute_from_path(response, "data")) < local_page_size:
                break
            set_attribute_from_path(
                kwargs, "body.page.cursor", get_attribute_from_path(response, "meta.page.after"), endpoint.params_map
            )

    def update_security_filter(
        self,
        security_filter_id: str,
        body: SecurityFilterUpdateRequest,
    ) -> SecurityFilterResponse:
        """Update a security filter.

        Update a specific security filter.
        Returns the security filter object when the request is successful.

        :param security_filter_id: The ID of the security filter.
        :type security_filter_id: str
        :param body: New definition of the security filter.
        :type body: SecurityFilterUpdateRequest
        :rtype: SecurityFilterResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["security_filter_id"] = security_filter_id

        kwargs["body"] = body

        return self._update_security_filter_endpoint.call_with_http_info(**kwargs)

    def update_security_monitoring_rule(
        self,
        rule_id: str,
        body: SecurityMonitoringRuleUpdatePayload,
    ) -> SecurityMonitoringRuleResponse:
        """Update an existing rule.

        Update an existing rule. When updating ``cases`` , ``queries`` or ``options`` , the whole field
        must be included. For example, when modifying a query all queries must be included.
        Default rules can only be updated to be enabled and to change notifications.

        :param rule_id: The ID of the rule.
        :type rule_id: str
        :type body: SecurityMonitoringRuleUpdatePayload
        :rtype: SecurityMonitoringRuleResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["rule_id"] = rule_id

        kwargs["body"] = body

        return self._update_security_monitoring_rule_endpoint.call_with_http_info(**kwargs)
