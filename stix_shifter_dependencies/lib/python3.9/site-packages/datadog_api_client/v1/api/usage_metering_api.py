# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Any, Dict, List, Union
import warnings

from datadog_api_client.api_client import ApiClient, Endpoint as _Endpoint
from datadog_api_client.configuration import Configuration
from datadog_api_client.model_utils import (
    datetime,
    UnsetType,
    unset,
)
from datadog_api_client.v1.model.usage_custom_reports_response import UsageCustomReportsResponse
from datadog_api_client.v1.model.usage_sort_direction import UsageSortDirection
from datadog_api_client.v1.model.usage_sort import UsageSort
from datadog_api_client.v1.model.usage_specified_custom_reports_response import UsageSpecifiedCustomReportsResponse
from datadog_api_client.v1.model.usage_analyzed_logs_response import UsageAnalyzedLogsResponse
from datadog_api_client.v1.model.usage_attribution_response import UsageAttributionResponse
from datadog_api_client.v1.model.usage_attribution_supported_metrics import UsageAttributionSupportedMetrics
from datadog_api_client.v1.model.usage_attribution_sort import UsageAttributionSort
from datadog_api_client.v1.model.usage_audit_logs_response import UsageAuditLogsResponse
from datadog_api_client.v1.model.usage_lambda_response import UsageLambdaResponse
from datadog_api_client.v1.model.usage_billable_summary_response import UsageBillableSummaryResponse
from datadog_api_client.v1.model.usage_ci_visibility_response import UsageCIVisibilityResponse
from datadog_api_client.v1.model.usage_cloud_security_posture_management_response import (
    UsageCloudSecurityPostureManagementResponse,
)
from datadog_api_client.v1.model.usage_cws_response import UsageCWSResponse
from datadog_api_client.v1.model.usage_dbm_response import UsageDBMResponse
from datadog_api_client.v1.model.usage_fargate_response import UsageFargateResponse
from datadog_api_client.v1.model.usage_hosts_response import UsageHostsResponse
from datadog_api_client.v1.model.hourly_usage_attribution_response import HourlyUsageAttributionResponse
from datadog_api_client.v1.model.hourly_usage_attribution_usage_type import HourlyUsageAttributionUsageType
from datadog_api_client.v1.model.usage_incident_management_response import UsageIncidentManagementResponse
from datadog_api_client.v1.model.usage_indexed_spans_response import UsageIndexedSpansResponse
from datadog_api_client.v1.model.usage_ingested_spans_response import UsageIngestedSpansResponse
from datadog_api_client.v1.model.usage_iot_response import UsageIoTResponse
from datadog_api_client.v1.model.usage_logs_response import UsageLogsResponse
from datadog_api_client.v1.model.usage_logs_by_retention_response import UsageLogsByRetentionResponse
from datadog_api_client.v1.model.usage_logs_by_index_response import UsageLogsByIndexResponse
from datadog_api_client.v1.model.monthly_usage_attribution_response import MonthlyUsageAttributionResponse
from datadog_api_client.v1.model.monthly_usage_attribution_supported_metrics import (
    MonthlyUsageAttributionSupportedMetrics,
)
from datadog_api_client.v1.model.usage_network_flows_response import UsageNetworkFlowsResponse
from datadog_api_client.v1.model.usage_network_hosts_response import UsageNetworkHostsResponse
from datadog_api_client.v1.model.usage_online_archive_response import UsageOnlineArchiveResponse
from datadog_api_client.v1.model.usage_profiling_response import UsageProfilingResponse
from datadog_api_client.v1.model.usage_rum_units_response import UsageRumUnitsResponse
from datadog_api_client.v1.model.usage_rum_sessions_response import UsageRumSessionsResponse
from datadog_api_client.v1.model.usage_sds_response import UsageSDSResponse
from datadog_api_client.v1.model.usage_snmp_response import UsageSNMPResponse
from datadog_api_client.v1.model.usage_summary_response import UsageSummaryResponse
from datadog_api_client.v1.model.usage_synthetics_response import UsageSyntheticsResponse
from datadog_api_client.v1.model.usage_synthetics_api_response import UsageSyntheticsAPIResponse
from datadog_api_client.v1.model.usage_synthetics_browser_response import UsageSyntheticsBrowserResponse
from datadog_api_client.v1.model.usage_timeseries_response import UsageTimeseriesResponse
from datadog_api_client.v1.model.usage_top_avg_metrics_response import UsageTopAvgMetricsResponse


class UsageMeteringApi:
    """
    The usage metering API allows you to get hourly, daily, and
    monthly usage across multiple facets of Datadog.
    This API is available to all Pro and Enterprise customers.
    Usage is only accessible for `parent-level organizations <https://docs.datadoghq.com/account_management/multi_organization/>`_.

    **Note** : Usage data is delayed by up to 72 hours from when it was incurred.
    It is retained for 15 months.

    You can retrieve up to 24 hours of hourly usage data for multiple organizations,
    and up to two months of hourly usage data for a single organization in one request.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient(Configuration())
        self.api_client = api_client

        self._get_daily_custom_reports_endpoint = _Endpoint(
            settings={
                "response_type": (UsageCustomReportsResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v1/daily_custom_reports",
                "operation_id": "get_daily_custom_reports",
                "http_method": "GET",
                "version": "v1",
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
                "sort_dir": {
                    "openapi_types": (UsageSortDirection,),
                    "attribute": "sort_dir",
                    "location": "query",
                },
                "sort": {
                    "openapi_types": (UsageSort,),
                    "attribute": "sort",
                    "location": "query",
                },
            },
            headers_map={
                "accept": ["application/json;datetime-format=rfc3339"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._get_hourly_usage_attribution_endpoint = _Endpoint(
            settings={
                "response_type": (HourlyUsageAttributionResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v1/usage/hourly-attribution",
                "operation_id": "get_hourly_usage_attribution",
                "http_method": "GET",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "start_hr": {
                    "required": True,
                    "openapi_types": (datetime,),
                    "attribute": "start_hr",
                    "location": "query",
                },
                "end_hr": {
                    "openapi_types": (datetime,),
                    "attribute": "end_hr",
                    "location": "query",
                },
                "usage_type": {
                    "required": True,
                    "openapi_types": (HourlyUsageAttributionUsageType,),
                    "attribute": "usage_type",
                    "location": "query",
                },
                "next_record_id": {
                    "openapi_types": (str,),
                    "attribute": "next_record_id",
                    "location": "query",
                },
                "tag_breakdown_keys": {
                    "openapi_types": (str,),
                    "attribute": "tag_breakdown_keys",
                    "location": "query",
                },
                "include_descendants": {
                    "openapi_types": (bool,),
                    "attribute": "include_descendants",
                    "location": "query",
                },
            },
            headers_map={
                "accept": ["application/json;datetime-format=rfc3339"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._get_incident_management_endpoint = _Endpoint(
            settings={
                "response_type": (UsageIncidentManagementResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v1/usage/incident-management",
                "operation_id": "get_incident_management",
                "http_method": "GET",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "start_hr": {
                    "required": True,
                    "openapi_types": (datetime,),
                    "attribute": "start_hr",
                    "location": "query",
                },
                "end_hr": {
                    "openapi_types": (datetime,),
                    "attribute": "end_hr",
                    "location": "query",
                },
            },
            headers_map={
                "accept": ["application/json;datetime-format=rfc3339"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._get_ingested_spans_endpoint = _Endpoint(
            settings={
                "response_type": (UsageIngestedSpansResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v1/usage/ingested-spans",
                "operation_id": "get_ingested_spans",
                "http_method": "GET",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "start_hr": {
                    "required": True,
                    "openapi_types": (datetime,),
                    "attribute": "start_hr",
                    "location": "query",
                },
                "end_hr": {
                    "openapi_types": (datetime,),
                    "attribute": "end_hr",
                    "location": "query",
                },
            },
            headers_map={
                "accept": ["application/json;datetime-format=rfc3339"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._get_monthly_custom_reports_endpoint = _Endpoint(
            settings={
                "response_type": (UsageCustomReportsResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v1/monthly_custom_reports",
                "operation_id": "get_monthly_custom_reports",
                "http_method": "GET",
                "version": "v1",
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
                "sort_dir": {
                    "openapi_types": (UsageSortDirection,),
                    "attribute": "sort_dir",
                    "location": "query",
                },
                "sort": {
                    "openapi_types": (UsageSort,),
                    "attribute": "sort",
                    "location": "query",
                },
            },
            headers_map={
                "accept": ["application/json;datetime-format=rfc3339"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._get_monthly_usage_attribution_endpoint = _Endpoint(
            settings={
                "response_type": (MonthlyUsageAttributionResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v1/usage/monthly-attribution",
                "operation_id": "get_monthly_usage_attribution",
                "http_method": "GET",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "start_month": {
                    "required": True,
                    "openapi_types": (datetime,),
                    "attribute": "start_month",
                    "location": "query",
                },
                "end_month": {
                    "openapi_types": (datetime,),
                    "attribute": "end_month",
                    "location": "query",
                },
                "fields": {
                    "required": True,
                    "openapi_types": (MonthlyUsageAttributionSupportedMetrics,),
                    "attribute": "fields",
                    "location": "query",
                },
                "sort_direction": {
                    "openapi_types": (UsageSortDirection,),
                    "attribute": "sort_direction",
                    "location": "query",
                },
                "sort_name": {
                    "openapi_types": (MonthlyUsageAttributionSupportedMetrics,),
                    "attribute": "sort_name",
                    "location": "query",
                },
                "tag_breakdown_keys": {
                    "openapi_types": (str,),
                    "attribute": "tag_breakdown_keys",
                    "location": "query",
                },
                "next_record_id": {
                    "openapi_types": (str,),
                    "attribute": "next_record_id",
                    "location": "query",
                },
                "include_descendants": {
                    "openapi_types": (bool,),
                    "attribute": "include_descendants",
                    "location": "query",
                },
            },
            headers_map={
                "accept": ["application/json;datetime-format=rfc3339"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._get_specified_daily_custom_reports_endpoint = _Endpoint(
            settings={
                "response_type": (UsageSpecifiedCustomReportsResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v1/daily_custom_reports/{report_id}",
                "operation_id": "get_specified_daily_custom_reports",
                "http_method": "GET",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "report_id": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "report_id",
                    "location": "path",
                },
            },
            headers_map={
                "accept": ["application/json;datetime-format=rfc3339"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._get_specified_monthly_custom_reports_endpoint = _Endpoint(
            settings={
                "response_type": (UsageSpecifiedCustomReportsResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v1/monthly_custom_reports/{report_id}",
                "operation_id": "get_specified_monthly_custom_reports",
                "http_method": "GET",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "report_id": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "report_id",
                    "location": "path",
                },
            },
            headers_map={
                "accept": ["application/json;datetime-format=rfc3339"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._get_usage_analyzed_logs_endpoint = _Endpoint(
            settings={
                "response_type": (UsageAnalyzedLogsResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v1/usage/analyzed_logs",
                "operation_id": "get_usage_analyzed_logs",
                "http_method": "GET",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "start_hr": {
                    "required": True,
                    "openapi_types": (datetime,),
                    "attribute": "start_hr",
                    "location": "query",
                },
                "end_hr": {
                    "openapi_types": (datetime,),
                    "attribute": "end_hr",
                    "location": "query",
                },
            },
            headers_map={
                "accept": ["application/json;datetime-format=rfc3339"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._get_usage_attribution_endpoint = _Endpoint(
            settings={
                "response_type": (UsageAttributionResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v1/usage/attribution",
                "operation_id": "get_usage_attribution",
                "http_method": "GET",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "start_month": {
                    "required": True,
                    "openapi_types": (datetime,),
                    "attribute": "start_month",
                    "location": "query",
                },
                "fields": {
                    "required": True,
                    "openapi_types": (UsageAttributionSupportedMetrics,),
                    "attribute": "fields",
                    "location": "query",
                },
                "end_month": {
                    "openapi_types": (datetime,),
                    "attribute": "end_month",
                    "location": "query",
                },
                "sort_direction": {
                    "openapi_types": (UsageSortDirection,),
                    "attribute": "sort_direction",
                    "location": "query",
                },
                "sort_name": {
                    "openapi_types": (UsageAttributionSort,),
                    "attribute": "sort_name",
                    "location": "query",
                },
                "include_descendants": {
                    "openapi_types": (bool,),
                    "attribute": "include_descendants",
                    "location": "query",
                },
                "offset": {
                    "openapi_types": (int,),
                    "attribute": "offset",
                    "location": "query",
                },
                "limit": {
                    "openapi_types": (int,),
                    "attribute": "limit",
                    "location": "query",
                },
            },
            headers_map={
                "accept": ["application/json;datetime-format=rfc3339"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._get_usage_audit_logs_endpoint = _Endpoint(
            settings={
                "response_type": (UsageAuditLogsResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v1/usage/audit_logs",
                "operation_id": "get_usage_audit_logs",
                "http_method": "GET",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "start_hr": {
                    "required": True,
                    "openapi_types": (datetime,),
                    "attribute": "start_hr",
                    "location": "query",
                },
                "end_hr": {
                    "openapi_types": (datetime,),
                    "attribute": "end_hr",
                    "location": "query",
                },
            },
            headers_map={
                "accept": ["application/json;datetime-format=rfc3339"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._get_usage_billable_summary_endpoint = _Endpoint(
            settings={
                "response_type": (UsageBillableSummaryResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v1/usage/billable-summary",
                "operation_id": "get_usage_billable_summary",
                "http_method": "GET",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "month": {
                    "openapi_types": (datetime,),
                    "attribute": "month",
                    "location": "query",
                },
            },
            headers_map={
                "accept": ["application/json;datetime-format=rfc3339"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._get_usage_ci_app_endpoint = _Endpoint(
            settings={
                "response_type": (UsageCIVisibilityResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v1/usage/ci-app",
                "operation_id": "get_usage_ci_app",
                "http_method": "GET",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "start_hr": {
                    "required": True,
                    "openapi_types": (datetime,),
                    "attribute": "start_hr",
                    "location": "query",
                },
                "end_hr": {
                    "openapi_types": (datetime,),
                    "attribute": "end_hr",
                    "location": "query",
                },
            },
            headers_map={
                "accept": ["application/json;datetime-format=rfc3339"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._get_usage_cloud_security_posture_management_endpoint = _Endpoint(
            settings={
                "response_type": (UsageCloudSecurityPostureManagementResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v1/usage/cspm",
                "operation_id": "get_usage_cloud_security_posture_management",
                "http_method": "GET",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "start_hr": {
                    "required": True,
                    "openapi_types": (datetime,),
                    "attribute": "start_hr",
                    "location": "query",
                },
                "end_hr": {
                    "openapi_types": (datetime,),
                    "attribute": "end_hr",
                    "location": "query",
                },
            },
            headers_map={
                "accept": ["application/json;datetime-format=rfc3339"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._get_usage_cws_endpoint = _Endpoint(
            settings={
                "response_type": (UsageCWSResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v1/usage/cws",
                "operation_id": "get_usage_cws",
                "http_method": "GET",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "start_hr": {
                    "required": True,
                    "openapi_types": (datetime,),
                    "attribute": "start_hr",
                    "location": "query",
                },
                "end_hr": {
                    "openapi_types": (datetime,),
                    "attribute": "end_hr",
                    "location": "query",
                },
            },
            headers_map={
                "accept": ["application/json;datetime-format=rfc3339"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._get_usage_dbm_endpoint = _Endpoint(
            settings={
                "response_type": (UsageDBMResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v1/usage/dbm",
                "operation_id": "get_usage_dbm",
                "http_method": "GET",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "start_hr": {
                    "required": True,
                    "openapi_types": (datetime,),
                    "attribute": "start_hr",
                    "location": "query",
                },
                "end_hr": {
                    "openapi_types": (datetime,),
                    "attribute": "end_hr",
                    "location": "query",
                },
            },
            headers_map={
                "accept": ["application/json;datetime-format=rfc3339"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._get_usage_fargate_endpoint = _Endpoint(
            settings={
                "response_type": (UsageFargateResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v1/usage/fargate",
                "operation_id": "get_usage_fargate",
                "http_method": "GET",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "start_hr": {
                    "required": True,
                    "openapi_types": (datetime,),
                    "attribute": "start_hr",
                    "location": "query",
                },
                "end_hr": {
                    "openapi_types": (datetime,),
                    "attribute": "end_hr",
                    "location": "query",
                },
            },
            headers_map={
                "accept": ["application/json;datetime-format=rfc3339"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._get_usage_hosts_endpoint = _Endpoint(
            settings={
                "response_type": (UsageHostsResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v1/usage/hosts",
                "operation_id": "get_usage_hosts",
                "http_method": "GET",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "start_hr": {
                    "required": True,
                    "openapi_types": (datetime,),
                    "attribute": "start_hr",
                    "location": "query",
                },
                "end_hr": {
                    "openapi_types": (datetime,),
                    "attribute": "end_hr",
                    "location": "query",
                },
            },
            headers_map={
                "accept": ["application/json;datetime-format=rfc3339"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._get_usage_indexed_spans_endpoint = _Endpoint(
            settings={
                "response_type": (UsageIndexedSpansResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v1/usage/indexed-spans",
                "operation_id": "get_usage_indexed_spans",
                "http_method": "GET",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "start_hr": {
                    "required": True,
                    "openapi_types": (datetime,),
                    "attribute": "start_hr",
                    "location": "query",
                },
                "end_hr": {
                    "openapi_types": (datetime,),
                    "attribute": "end_hr",
                    "location": "query",
                },
            },
            headers_map={
                "accept": ["application/json;datetime-format=rfc3339"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._get_usage_internet_of_things_endpoint = _Endpoint(
            settings={
                "response_type": (UsageIoTResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v1/usage/iot",
                "operation_id": "get_usage_internet_of_things",
                "http_method": "GET",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "start_hr": {
                    "required": True,
                    "openapi_types": (datetime,),
                    "attribute": "start_hr",
                    "location": "query",
                },
                "end_hr": {
                    "openapi_types": (datetime,),
                    "attribute": "end_hr",
                    "location": "query",
                },
            },
            headers_map={
                "accept": ["application/json;datetime-format=rfc3339"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._get_usage_lambda_endpoint = _Endpoint(
            settings={
                "response_type": (UsageLambdaResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v1/usage/aws_lambda",
                "operation_id": "get_usage_lambda",
                "http_method": "GET",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "start_hr": {
                    "required": True,
                    "openapi_types": (datetime,),
                    "attribute": "start_hr",
                    "location": "query",
                },
                "end_hr": {
                    "openapi_types": (datetime,),
                    "attribute": "end_hr",
                    "location": "query",
                },
            },
            headers_map={
                "accept": ["application/json;datetime-format=rfc3339"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._get_usage_logs_endpoint = _Endpoint(
            settings={
                "response_type": (UsageLogsResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v1/usage/logs",
                "operation_id": "get_usage_logs",
                "http_method": "GET",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "start_hr": {
                    "required": True,
                    "openapi_types": (datetime,),
                    "attribute": "start_hr",
                    "location": "query",
                },
                "end_hr": {
                    "openapi_types": (datetime,),
                    "attribute": "end_hr",
                    "location": "query",
                },
            },
            headers_map={
                "accept": ["application/json;datetime-format=rfc3339"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._get_usage_logs_by_index_endpoint = _Endpoint(
            settings={
                "response_type": (UsageLogsByIndexResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v1/usage/logs_by_index",
                "operation_id": "get_usage_logs_by_index",
                "http_method": "GET",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "start_hr": {
                    "required": True,
                    "openapi_types": (datetime,),
                    "attribute": "start_hr",
                    "location": "query",
                },
                "end_hr": {
                    "openapi_types": (datetime,),
                    "attribute": "end_hr",
                    "location": "query",
                },
                "index_name": {
                    "openapi_types": ([str],),
                    "attribute": "index_name",
                    "location": "query",
                    "collection_format": "multi",
                },
            },
            headers_map={
                "accept": ["application/json;datetime-format=rfc3339"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._get_usage_logs_by_retention_endpoint = _Endpoint(
            settings={
                "response_type": (UsageLogsByRetentionResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v1/usage/logs-by-retention",
                "operation_id": "get_usage_logs_by_retention",
                "http_method": "GET",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "start_hr": {
                    "required": True,
                    "openapi_types": (datetime,),
                    "attribute": "start_hr",
                    "location": "query",
                },
                "end_hr": {
                    "openapi_types": (datetime,),
                    "attribute": "end_hr",
                    "location": "query",
                },
            },
            headers_map={
                "accept": ["application/json;datetime-format=rfc3339"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._get_usage_network_flows_endpoint = _Endpoint(
            settings={
                "response_type": (UsageNetworkFlowsResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v1/usage/network_flows",
                "operation_id": "get_usage_network_flows",
                "http_method": "GET",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "start_hr": {
                    "required": True,
                    "openapi_types": (datetime,),
                    "attribute": "start_hr",
                    "location": "query",
                },
                "end_hr": {
                    "openapi_types": (datetime,),
                    "attribute": "end_hr",
                    "location": "query",
                },
            },
            headers_map={
                "accept": ["application/json;datetime-format=rfc3339"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._get_usage_network_hosts_endpoint = _Endpoint(
            settings={
                "response_type": (UsageNetworkHostsResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v1/usage/network_hosts",
                "operation_id": "get_usage_network_hosts",
                "http_method": "GET",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "start_hr": {
                    "required": True,
                    "openapi_types": (datetime,),
                    "attribute": "start_hr",
                    "location": "query",
                },
                "end_hr": {
                    "openapi_types": (datetime,),
                    "attribute": "end_hr",
                    "location": "query",
                },
            },
            headers_map={
                "accept": ["application/json;datetime-format=rfc3339"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._get_usage_online_archive_endpoint = _Endpoint(
            settings={
                "response_type": (UsageOnlineArchiveResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v1/usage/online-archive",
                "operation_id": "get_usage_online_archive",
                "http_method": "GET",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "start_hr": {
                    "required": True,
                    "openapi_types": (datetime,),
                    "attribute": "start_hr",
                    "location": "query",
                },
                "end_hr": {
                    "openapi_types": (datetime,),
                    "attribute": "end_hr",
                    "location": "query",
                },
            },
            headers_map={
                "accept": ["application/json;datetime-format=rfc3339"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._get_usage_profiling_endpoint = _Endpoint(
            settings={
                "response_type": (UsageProfilingResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v1/usage/profiling",
                "operation_id": "get_usage_profiling",
                "http_method": "GET",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "start_hr": {
                    "required": True,
                    "openapi_types": (datetime,),
                    "attribute": "start_hr",
                    "location": "query",
                },
                "end_hr": {
                    "openapi_types": (datetime,),
                    "attribute": "end_hr",
                    "location": "query",
                },
            },
            headers_map={
                "accept": ["application/json;datetime-format=rfc3339"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._get_usage_rum_sessions_endpoint = _Endpoint(
            settings={
                "response_type": (UsageRumSessionsResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v1/usage/rum_sessions",
                "operation_id": "get_usage_rum_sessions",
                "http_method": "GET",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "start_hr": {
                    "required": True,
                    "openapi_types": (datetime,),
                    "attribute": "start_hr",
                    "location": "query",
                },
                "end_hr": {
                    "openapi_types": (datetime,),
                    "attribute": "end_hr",
                    "location": "query",
                },
                "type": {
                    "openapi_types": (str,),
                    "attribute": "type",
                    "location": "query",
                },
            },
            headers_map={
                "accept": ["application/json;datetime-format=rfc3339"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._get_usage_rum_units_endpoint = _Endpoint(
            settings={
                "response_type": (UsageRumUnitsResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v1/usage/rum",
                "operation_id": "get_usage_rum_units",
                "http_method": "GET",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "start_hr": {
                    "required": True,
                    "openapi_types": (datetime,),
                    "attribute": "start_hr",
                    "location": "query",
                },
                "end_hr": {
                    "openapi_types": (datetime,),
                    "attribute": "end_hr",
                    "location": "query",
                },
            },
            headers_map={
                "accept": ["application/json;datetime-format=rfc3339"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._get_usage_sds_endpoint = _Endpoint(
            settings={
                "response_type": (UsageSDSResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v1/usage/sds",
                "operation_id": "get_usage_sds",
                "http_method": "GET",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "start_hr": {
                    "required": True,
                    "openapi_types": (datetime,),
                    "attribute": "start_hr",
                    "location": "query",
                },
                "end_hr": {
                    "openapi_types": (datetime,),
                    "attribute": "end_hr",
                    "location": "query",
                },
            },
            headers_map={
                "accept": ["application/json;datetime-format=rfc3339"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._get_usage_snmp_endpoint = _Endpoint(
            settings={
                "response_type": (UsageSNMPResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v1/usage/snmp",
                "operation_id": "get_usage_snmp",
                "http_method": "GET",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "start_hr": {
                    "required": True,
                    "openapi_types": (datetime,),
                    "attribute": "start_hr",
                    "location": "query",
                },
                "end_hr": {
                    "openapi_types": (datetime,),
                    "attribute": "end_hr",
                    "location": "query",
                },
            },
            headers_map={
                "accept": ["application/json;datetime-format=rfc3339"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._get_usage_summary_endpoint = _Endpoint(
            settings={
                "response_type": (UsageSummaryResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v1/usage/summary",
                "operation_id": "get_usage_summary",
                "http_method": "GET",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "start_month": {
                    "required": True,
                    "openapi_types": (datetime,),
                    "attribute": "start_month",
                    "location": "query",
                },
                "end_month": {
                    "openapi_types": (datetime,),
                    "attribute": "end_month",
                    "location": "query",
                },
                "include_org_details": {
                    "openapi_types": (bool,),
                    "attribute": "include_org_details",
                    "location": "query",
                },
            },
            headers_map={
                "accept": ["application/json;datetime-format=rfc3339"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._get_usage_synthetics_endpoint = _Endpoint(
            settings={
                "response_type": (UsageSyntheticsResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v1/usage/synthetics",
                "operation_id": "get_usage_synthetics",
                "http_method": "GET",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "start_hr": {
                    "required": True,
                    "openapi_types": (datetime,),
                    "attribute": "start_hr",
                    "location": "query",
                },
                "end_hr": {
                    "openapi_types": (datetime,),
                    "attribute": "end_hr",
                    "location": "query",
                },
            },
            headers_map={
                "accept": ["application/json;datetime-format=rfc3339"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._get_usage_synthetics_api_endpoint = _Endpoint(
            settings={
                "response_type": (UsageSyntheticsAPIResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v1/usage/synthetics_api",
                "operation_id": "get_usage_synthetics_api",
                "http_method": "GET",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "start_hr": {
                    "required": True,
                    "openapi_types": (datetime,),
                    "attribute": "start_hr",
                    "location": "query",
                },
                "end_hr": {
                    "openapi_types": (datetime,),
                    "attribute": "end_hr",
                    "location": "query",
                },
            },
            headers_map={
                "accept": ["application/json;datetime-format=rfc3339"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._get_usage_synthetics_browser_endpoint = _Endpoint(
            settings={
                "response_type": (UsageSyntheticsBrowserResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v1/usage/synthetics_browser",
                "operation_id": "get_usage_synthetics_browser",
                "http_method": "GET",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "start_hr": {
                    "required": True,
                    "openapi_types": (datetime,),
                    "attribute": "start_hr",
                    "location": "query",
                },
                "end_hr": {
                    "openapi_types": (datetime,),
                    "attribute": "end_hr",
                    "location": "query",
                },
            },
            headers_map={
                "accept": ["application/json;datetime-format=rfc3339"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._get_usage_timeseries_endpoint = _Endpoint(
            settings={
                "response_type": (UsageTimeseriesResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v1/usage/timeseries",
                "operation_id": "get_usage_timeseries",
                "http_method": "GET",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "start_hr": {
                    "required": True,
                    "openapi_types": (datetime,),
                    "attribute": "start_hr",
                    "location": "query",
                },
                "end_hr": {
                    "openapi_types": (datetime,),
                    "attribute": "end_hr",
                    "location": "query",
                },
            },
            headers_map={
                "accept": ["application/json;datetime-format=rfc3339"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._get_usage_top_avg_metrics_endpoint = _Endpoint(
            settings={
                "response_type": (UsageTopAvgMetricsResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v1/usage/top_avg_metrics",
                "operation_id": "get_usage_top_avg_metrics",
                "http_method": "GET",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "month": {
                    "openapi_types": (datetime,),
                    "attribute": "month",
                    "location": "query",
                },
                "day": {
                    "openapi_types": (datetime,),
                    "attribute": "day",
                    "location": "query",
                },
                "names": {
                    "openapi_types": ([str],),
                    "attribute": "names",
                    "location": "query",
                    "collection_format": "multi",
                },
                "limit": {
                    "validation": {
                        "inclusive_maximum": 5000,
                        "inclusive_minimum": 1,
                    },
                    "openapi_types": (int,),
                    "attribute": "limit",
                    "location": "query",
                },
                "next_record_id": {
                    "openapi_types": (str,),
                    "attribute": "next_record_id",
                    "location": "query",
                },
            },
            headers_map={
                "accept": ["application/json;datetime-format=rfc3339"],
                "content_type": [],
            },
            api_client=api_client,
        )

    def get_daily_custom_reports(
        self,
        *,
        page_size: Union[int, UnsetType] = unset,
        page_number: Union[int, UnsetType] = unset,
        sort_dir: Union[UsageSortDirection, UnsetType] = unset,
        sort: Union[UsageSort, UnsetType] = unset,
    ) -> UsageCustomReportsResponse:
        """Get the list of available daily custom reports. **Deprecated**.

        Get daily custom reports.
        **Note:** This endpoint will be fully deprecated on December 1, 2022.
        Refer to `Migrating from v1 to v2 of the Usage Attribution API <https://docs.datadoghq.com/account_management/guide/usage-attribution-migration/>`_ for the associated migration guide.

        :param page_size: The number of files to return in the response. ``[default=60]``.
        :type page_size: int, optional
        :param page_number: The identifier of the first page to return. This parameter is used for the pagination feature ``[default=0]``.
        :type page_number: int, optional
        :param sort_dir: The direction to sort by: ``[desc, asc]``.
        :type sort_dir: UsageSortDirection, optional
        :param sort: The field to sort by: ``[computed_on, size, start_date, end_date]``.
        :type sort: UsageSort, optional
        :rtype: UsageCustomReportsResponse
        """
        kwargs: Dict[str, Any] = {}
        if page_size is not unset:
            kwargs["page_size"] = page_size

        if page_number is not unset:
            kwargs["page_number"] = page_number

        if sort_dir is not unset:
            kwargs["sort_dir"] = sort_dir

        if sort is not unset:
            kwargs["sort"] = sort

        warnings.warn("get_daily_custom_reports is deprecated", DeprecationWarning, stacklevel=2)
        return self._get_daily_custom_reports_endpoint.call_with_http_info(**kwargs)

    def get_hourly_usage_attribution(
        self,
        start_hr: datetime,
        usage_type: HourlyUsageAttributionUsageType,
        *,
        end_hr: Union[datetime, UnsetType] = unset,
        next_record_id: Union[str, UnsetType] = unset,
        tag_breakdown_keys: Union[str, UnsetType] = unset,
        include_descendants: Union[bool, UnsetType] = unset,
    ) -> HourlyUsageAttributionResponse:
        """Get hourly usage attribution.

        Get hourly usage attribution. Multi-region data is available starting March 1, 2023.

        This API endpoint is paginated. To make sure you receive all records, check if the value of ``next_record_id`` is
        set in the response. If it is, make another request and pass ``next_record_id`` as a parameter.
        Pseudo code example:

        .. code-block::

           response := GetHourlyUsageAttribution(start_month)
           cursor := response.metadata.pagination.next_record_id
           WHILE cursor != null BEGIN
             sleep(5 seconds)  # Avoid running into rate limit
             response := GetHourlyUsageAttribution(start_month, next_record_id=cursor)
             cursor := response.metadata.pagination.next_record_id
           END

        :param start_hr: Datetime in ISO-8601 format, UTC, precise to hour: ``[YYYY-MM-DDThh]`` for usage beginning at this hour.
        :type start_hr: datetime
        :param usage_type: Usage type to retrieve.
        :type usage_type: HourlyUsageAttributionUsageType
        :param end_hr: Datetime in ISO-8601 format, UTC, precise to hour: ``[YYYY-MM-DDThh]`` for usage ending
            **before** this hour.
        :type end_hr: datetime, optional
        :param next_record_id: List following results with a next_record_id provided in the previous query.
        :type next_record_id: str, optional
        :param tag_breakdown_keys: Comma separated list of tags used to group usage. If no value is provided the usage will not be broken down by tags.

            To see which tags are available, look for the value of ``tag_config_source`` in the API response.
        :type tag_breakdown_keys: str, optional
        :param include_descendants: Include child org usage in the response. Defaults to ``true``.
        :type include_descendants: bool, optional
        :rtype: HourlyUsageAttributionResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["start_hr"] = start_hr

        if end_hr is not unset:
            kwargs["end_hr"] = end_hr

        kwargs["usage_type"] = usage_type

        if next_record_id is not unset:
            kwargs["next_record_id"] = next_record_id

        if tag_breakdown_keys is not unset:
            kwargs["tag_breakdown_keys"] = tag_breakdown_keys

        if include_descendants is not unset:
            kwargs["include_descendants"] = include_descendants

        return self._get_hourly_usage_attribution_endpoint.call_with_http_info(**kwargs)

    def get_incident_management(
        self,
        start_hr: datetime,
        *,
        end_hr: Union[datetime, UnsetType] = unset,
    ) -> UsageIncidentManagementResponse:
        """Get hourly usage for incident management.

        Get hourly usage for incident management.
        **Note:** hourly usage data for all products is now available in the `Get hourly usage by product family API <https://docs.datadoghq.com/api/latest/usage-metering/#get-hourly-usage-by-product-family>`_. Refer to `Migrating from the V1 Hourly Usage APIs to V2 <https://docs.datadoghq.com/account_management/guide/hourly-usage-migration/>`_ for the associated migration guide.

        :param start_hr: Datetime in ISO-8601 format, UTC, precise to hour: ``[YYYY-MM-DDThh]`` for usage beginning at this hour.
        :type start_hr: datetime
        :param end_hr: Datetime in ISO-8601 format, UTC, precise to hour: ``[YYYY-MM-DDThh]`` for usage ending
            **before** this hour.
        :type end_hr: datetime, optional
        :rtype: UsageIncidentManagementResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["start_hr"] = start_hr

        if end_hr is not unset:
            kwargs["end_hr"] = end_hr

        return self._get_incident_management_endpoint.call_with_http_info(**kwargs)

    def get_ingested_spans(
        self,
        start_hr: datetime,
        *,
        end_hr: Union[datetime, UnsetType] = unset,
    ) -> UsageIngestedSpansResponse:
        """Get hourly usage for ingested spans.

        Get hourly usage for ingested spans.
        **Note:** hourly usage data for all products is now available in the `Get hourly usage by product family API <https://docs.datadoghq.com/api/latest/usage-metering/#get-hourly-usage-by-product-family>`_. Refer to `Migrating from the V1 Hourly Usage APIs to V2 <https://docs.datadoghq.com/account_management/guide/hourly-usage-migration/>`_ for the associated migration guide.

        :param start_hr: Datetime in ISO-8601 format, UTC, precise to hour: ``[YYYY-MM-DDThh]`` for usage beginning at this hour.
        :type start_hr: datetime
        :param end_hr: Datetime in ISO-8601 format, UTC, precise to hour: ``[YYYY-MM-DDThh]`` for usage ending
            **before** this hour.
        :type end_hr: datetime, optional
        :rtype: UsageIngestedSpansResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["start_hr"] = start_hr

        if end_hr is not unset:
            kwargs["end_hr"] = end_hr

        return self._get_ingested_spans_endpoint.call_with_http_info(**kwargs)

    def get_monthly_custom_reports(
        self,
        *,
        page_size: Union[int, UnsetType] = unset,
        page_number: Union[int, UnsetType] = unset,
        sort_dir: Union[UsageSortDirection, UnsetType] = unset,
        sort: Union[UsageSort, UnsetType] = unset,
    ) -> UsageCustomReportsResponse:
        """Get the list of available monthly custom reports. **Deprecated**.

        Get monthly custom reports.
        **Note:** This endpoint will be fully deprecated on December 1, 2022.
        Refer to `Migrating from v1 to v2 of the Usage Attribution API <https://docs.datadoghq.com/account_management/guide/usage-attribution-migration/>`_ for the associated migration guide.

        :param page_size: The number of files to return in the response ``[default=60].``
        :type page_size: int, optional
        :param page_number: The identifier of the first page to return. This parameter is used for the pagination feature ``[default=0]``.
        :type page_number: int, optional
        :param sort_dir: The direction to sort by: ``[desc, asc]``.
        :type sort_dir: UsageSortDirection, optional
        :param sort: The field to sort by: ``[computed_on, size, start_date, end_date]``.
        :type sort: UsageSort, optional
        :rtype: UsageCustomReportsResponse
        """
        kwargs: Dict[str, Any] = {}
        if page_size is not unset:
            kwargs["page_size"] = page_size

        if page_number is not unset:
            kwargs["page_number"] = page_number

        if sort_dir is not unset:
            kwargs["sort_dir"] = sort_dir

        if sort is not unset:
            kwargs["sort"] = sort

        warnings.warn("get_monthly_custom_reports is deprecated", DeprecationWarning, stacklevel=2)
        return self._get_monthly_custom_reports_endpoint.call_with_http_info(**kwargs)

    def get_monthly_usage_attribution(
        self,
        start_month: datetime,
        fields: MonthlyUsageAttributionSupportedMetrics,
        *,
        end_month: Union[datetime, UnsetType] = unset,
        sort_direction: Union[UsageSortDirection, UnsetType] = unset,
        sort_name: Union[MonthlyUsageAttributionSupportedMetrics, UnsetType] = unset,
        tag_breakdown_keys: Union[str, UnsetType] = unset,
        next_record_id: Union[str, UnsetType] = unset,
        include_descendants: Union[bool, UnsetType] = unset,
    ) -> MonthlyUsageAttributionResponse:
        """Get monthly usage attribution.

        Get monthly usage attribution. Multi-region data is available starting March 1, 2023.

        This API endpoint is paginated. To make sure you receive all records, check if the value of ``next_record_id`` is
        set in the response. If it is, make another request and pass ``next_record_id`` as a parameter.
        Pseudo code example:

        .. code-block::

           response := GetMonthlyUsageAttribution(start_month)
           cursor := response.metadata.pagination.next_record_id
           WHILE cursor != null BEGIN
             sleep(5 seconds)  # Avoid running into rate limit
             response := GetMonthlyUsageAttribution(start_month, next_record_id=cursor)
             cursor := response.metadata.pagination.next_record_id
           END

        :param start_month: Datetime in ISO-8601 format, UTC, precise to month: ``[YYYY-MM]`` for usage beginning in this month.
            Maximum of 15 months ago.
        :type start_month: datetime
        :param fields: Comma-separated list of usage types to return, or ``*`` for all usage types.
        :type fields: MonthlyUsageAttributionSupportedMetrics
        :param end_month: Datetime in ISO-8601 format, UTC, precise to month: ``[YYYY-MM]`` for usage ending this month.
        :type end_month: datetime, optional
        :param sort_direction: The direction to sort by: ``[desc, asc]``.
        :type sort_direction: UsageSortDirection, optional
        :param sort_name: The field to sort by.
        :type sort_name: MonthlyUsageAttributionSupportedMetrics, optional
        :param tag_breakdown_keys: Comma separated list of tag keys used to group usage. If no value is provided the usage will not be broken down by tags.

            To see which tags are available, look for the value of ``tag_config_source`` in the API response.
        :type tag_breakdown_keys: str, optional
        :param next_record_id: List following results with a next_record_id provided in the previous query.
        :type next_record_id: str, optional
        :param include_descendants: Include child org usage in the response. Defaults to ``true``.
        :type include_descendants: bool, optional
        :rtype: MonthlyUsageAttributionResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["start_month"] = start_month

        if end_month is not unset:
            kwargs["end_month"] = end_month

        kwargs["fields"] = fields

        if sort_direction is not unset:
            kwargs["sort_direction"] = sort_direction

        if sort_name is not unset:
            kwargs["sort_name"] = sort_name

        if tag_breakdown_keys is not unset:
            kwargs["tag_breakdown_keys"] = tag_breakdown_keys

        if next_record_id is not unset:
            kwargs["next_record_id"] = next_record_id

        if include_descendants is not unset:
            kwargs["include_descendants"] = include_descendants

        return self._get_monthly_usage_attribution_endpoint.call_with_http_info(**kwargs)

    def get_specified_daily_custom_reports(
        self,
        report_id: str,
    ) -> UsageSpecifiedCustomReportsResponse:
        """Get specified daily custom reports. **Deprecated**.

        Get specified daily custom reports.
        **Note:** This endpoint will be fully deprecated on December 1, 2022.
        Refer to `Migrating from v1 to v2 of the Usage Attribution API <https://docs.datadoghq.com/account_management/guide/usage-attribution-migration/>`_ for the associated migration guide.

        :param report_id: Date of the report in the format ``YYYY-MM-DD``.
        :type report_id: str
        :rtype: UsageSpecifiedCustomReportsResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["report_id"] = report_id

        warnings.warn("get_specified_daily_custom_reports is deprecated", DeprecationWarning, stacklevel=2)
        return self._get_specified_daily_custom_reports_endpoint.call_with_http_info(**kwargs)

    def get_specified_monthly_custom_reports(
        self,
        report_id: str,
    ) -> UsageSpecifiedCustomReportsResponse:
        """Get specified monthly custom reports. **Deprecated**.

        Get specified monthly custom reports.
        **Note:** This endpoint will be fully deprecated on December 1, 2022.
        Refer to `Migrating from v1 to v2 of the Usage Attribution API <https://docs.datadoghq.com/account_management/guide/usage-attribution-migration/>`_ for the associated migration guide.

        :param report_id: Date of the report in the format ``YYYY-MM-DD``.
        :type report_id: str
        :rtype: UsageSpecifiedCustomReportsResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["report_id"] = report_id

        warnings.warn("get_specified_monthly_custom_reports is deprecated", DeprecationWarning, stacklevel=2)
        return self._get_specified_monthly_custom_reports_endpoint.call_with_http_info(**kwargs)

    def get_usage_analyzed_logs(
        self,
        start_hr: datetime,
        *,
        end_hr: Union[datetime, UnsetType] = unset,
    ) -> UsageAnalyzedLogsResponse:
        """Get hourly usage for analyzed logs.

        Get hourly usage for analyzed logs (Security Monitoring).
        **Note:** hourly usage data for all products is now available in the `Get hourly usage by product family API <https://docs.datadoghq.com/api/latest/usage-metering/#get-hourly-usage-by-product-family>`_. Refer to `Migrating from the V1 Hourly Usage APIs to V2 <https://docs.datadoghq.com/account_management/guide/hourly-usage-migration/>`_ for the associated migration guide.

        :param start_hr: Datetime in ISO-8601 format, UTC, precise to hour: ``[YYYY-MM-DDThh]`` for usage beginning at this hour.
        :type start_hr: datetime
        :param end_hr: Datetime in ISO-8601 format, UTC, precise to hour: ``[YYYY-MM-DDThh]`` for usage ending
            **before** this hour.
        :type end_hr: datetime, optional
        :rtype: UsageAnalyzedLogsResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["start_hr"] = start_hr

        if end_hr is not unset:
            kwargs["end_hr"] = end_hr

        return self._get_usage_analyzed_logs_endpoint.call_with_http_info(**kwargs)

    def get_usage_attribution(
        self,
        start_month: datetime,
        fields: UsageAttributionSupportedMetrics,
        *,
        end_month: Union[datetime, UnsetType] = unset,
        sort_direction: Union[UsageSortDirection, UnsetType] = unset,
        sort_name: Union[UsageAttributionSort, UnsetType] = unset,
        include_descendants: Union[bool, UnsetType] = unset,
        offset: Union[int, UnsetType] = unset,
        limit: Union[int, UnsetType] = unset,
    ) -> UsageAttributionResponse:
        """Get usage attribution. **Deprecated**.

        Get usage attribution.
        **Note:** This endpoint will be fully deprecated on December 1, 2022.
        Refer to `Migrating from v1 to v2 of the Usage Attribution API <https://docs.datadoghq.com/account_management/guide/usage-attribution-migration/>`_ for the associated migration guide.

        :param start_month: Datetime in ISO-8601 format, UTC, precise to month: ``[YYYY-MM]`` for usage beginning in this month.
            Maximum of 15 months ago.
        :type start_month: datetime
        :param fields: Comma-separated list of usage types to return, or ``*`` for all usage types.
        :type fields: UsageAttributionSupportedMetrics
        :param end_month: Datetime in ISO-8601 format, UTC, precise to month: ``[YYYY-MM]`` for usage ending this month.
        :type end_month: datetime, optional
        :param sort_direction: The direction to sort by: ``[desc, asc]``.
        :type sort_direction: UsageSortDirection, optional
        :param sort_name: The field to sort by.
        :type sort_name: UsageAttributionSort, optional
        :param include_descendants: Include child org usage in the response. Defaults to false.
        :type include_descendants: bool, optional
        :param offset: Number of records to skip before beginning to return.
        :type offset: int, optional
        :param limit: Maximum number of records to be returned.
        :type limit: int, optional
        :rtype: UsageAttributionResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["start_month"] = start_month

        kwargs["fields"] = fields

        if end_month is not unset:
            kwargs["end_month"] = end_month

        if sort_direction is not unset:
            kwargs["sort_direction"] = sort_direction

        if sort_name is not unset:
            kwargs["sort_name"] = sort_name

        if include_descendants is not unset:
            kwargs["include_descendants"] = include_descendants

        if offset is not unset:
            kwargs["offset"] = offset

        if limit is not unset:
            kwargs["limit"] = limit

        warnings.warn("get_usage_attribution is deprecated", DeprecationWarning, stacklevel=2)
        return self._get_usage_attribution_endpoint.call_with_http_info(**kwargs)

    def get_usage_audit_logs(
        self,
        start_hr: datetime,
        *,
        end_hr: Union[datetime, UnsetType] = unset,
    ) -> UsageAuditLogsResponse:
        """Get hourly usage for audit logs. **Deprecated**.

        Get hourly usage for audit logs.
        **Note:** This endpoint has been deprecated.

        :param start_hr: Datetime in ISO-8601 format, UTC, precise to hour: ``[YYYY-MM-DDThh]`` for usage beginning at this hour.
        :type start_hr: datetime
        :param end_hr: Datetime in ISO-8601 format, UTC, precise to hour: ``[YYYY-MM-DDThh]`` for usage ending
            **before** this hour.
        :type end_hr: datetime, optional
        :rtype: UsageAuditLogsResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["start_hr"] = start_hr

        if end_hr is not unset:
            kwargs["end_hr"] = end_hr

        warnings.warn("get_usage_audit_logs is deprecated", DeprecationWarning, stacklevel=2)
        return self._get_usage_audit_logs_endpoint.call_with_http_info(**kwargs)

    def get_usage_billable_summary(
        self,
        *,
        month: Union[datetime, UnsetType] = unset,
    ) -> UsageBillableSummaryResponse:
        """Get billable usage across your account.

        Get billable usage across your account.

        :param month: Datetime in ISO-8601 format, UTC, precise to month: ``[YYYY-MM]`` for usage starting this month.
        :type month: datetime, optional
        :rtype: UsageBillableSummaryResponse
        """
        kwargs: Dict[str, Any] = {}
        if month is not unset:
            kwargs["month"] = month

        return self._get_usage_billable_summary_endpoint.call_with_http_info(**kwargs)

    def get_usage_ci_app(
        self,
        start_hr: datetime,
        *,
        end_hr: Union[datetime, UnsetType] = unset,
    ) -> UsageCIVisibilityResponse:
        """Get hourly usage for CI visibility.

        Get hourly usage for CI visibility (tests, pipeline, and spans).
        **Note:** hourly usage data for all products is now available in the `Get hourly usage by product family API <https://docs.datadoghq.com/api/latest/usage-metering/#get-hourly-usage-by-product-family>`_. Refer to `Migrating from the V1 Hourly Usage APIs to V2 <https://docs.datadoghq.com/account_management/guide/hourly-usage-migration/>`_ for the associated migration guide.

        :param start_hr: Datetime in ISO-8601 format, UTC, precise to hour: ``[YYYY-MM-DDThh]`` for usage beginning at this hour.
        :type start_hr: datetime
        :param end_hr: Datetime in ISO-8601 format, UTC, precise to hour: ``[YYYY-MM-DDThh]`` for usage ending
            **before** this hour.
        :type end_hr: datetime, optional
        :rtype: UsageCIVisibilityResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["start_hr"] = start_hr

        if end_hr is not unset:
            kwargs["end_hr"] = end_hr

        return self._get_usage_ci_app_endpoint.call_with_http_info(**kwargs)

    def get_usage_cloud_security_posture_management(
        self,
        start_hr: datetime,
        *,
        end_hr: Union[datetime, UnsetType] = unset,
    ) -> UsageCloudSecurityPostureManagementResponse:
        """Get hourly usage for CSPM.

        Get hourly usage for cloud security posture management (CSPM).
        **Note:** hourly usage data for all products is now available in the `Get hourly usage by product family API <https://docs.datadoghq.com/api/latest/usage-metering/#get-hourly-usage-by-product-family>`_. Refer to `Migrating from the V1 Hourly Usage APIs to V2 <https://docs.datadoghq.com/account_management/guide/hourly-usage-migration/>`_ for the associated migration guide.

        :param start_hr: Datetime in ISO-8601 format, UTC, precise to hour: ``[YYYY-MM-DDThh]`` for usage beginning at this hour.
        :type start_hr: datetime
        :param end_hr: Datetime in ISO-8601 format, UTC, precise to hour: ``[YYYY-MM-DDThh]`` for usage ending
            **before** this hour.
        :type end_hr: datetime, optional
        :rtype: UsageCloudSecurityPostureManagementResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["start_hr"] = start_hr

        if end_hr is not unset:
            kwargs["end_hr"] = end_hr

        return self._get_usage_cloud_security_posture_management_endpoint.call_with_http_info(**kwargs)

    def get_usage_cws(
        self,
        start_hr: datetime,
        *,
        end_hr: Union[datetime, UnsetType] = unset,
    ) -> UsageCWSResponse:
        """Get hourly usage for cloud workload security.

        Get hourly usage for cloud workload security.
        **Note:** hourly usage data for all products is now available in the `Get hourly usage by product family API <https://docs.datadoghq.com/api/latest/usage-metering/#get-hourly-usage-by-product-family>`_. Refer to `Migrating from the V1 Hourly Usage APIs to V2 <https://docs.datadoghq.com/account_management/guide/hourly-usage-migration/>`_ for the associated migration guide.

        :param start_hr: Datetime in ISO-8601 format, UTC, precise to hour: ``[YYYY-MM-DDThh]`` for usage beginning at this hour.
        :type start_hr: datetime
        :param end_hr: Datetime in ISO-8601 format, UTC, precise to hour: ``[YYYY-MM-DDThh]`` for usage ending
            **before** this hour.
        :type end_hr: datetime, optional
        :rtype: UsageCWSResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["start_hr"] = start_hr

        if end_hr is not unset:
            kwargs["end_hr"] = end_hr

        return self._get_usage_cws_endpoint.call_with_http_info(**kwargs)

    def get_usage_dbm(
        self,
        start_hr: datetime,
        *,
        end_hr: Union[datetime, UnsetType] = unset,
    ) -> UsageDBMResponse:
        """Get hourly usage for database monitoring.

        Get hourly usage for database monitoring
        **Note:** hourly usage data for all products is now available in the `Get hourly usage by product family API <https://docs.datadoghq.com/api/latest/usage-metering/#get-hourly-usage-by-product-family>`_. Refer to `Migrating from the V1 Hourly Usage APIs to V2 <https://docs.datadoghq.com/account_management/guide/hourly-usage-migration/>`_ for the associated migration guide.

        :param start_hr: Datetime in ISO-8601 format, UTC, precise to hour: ``[YYYY-MM-DDThh]`` for usage beginning at this hour.
        :type start_hr: datetime
        :param end_hr: Datetime in ISO-8601 format, UTC, precise to hour: ``[YYYY-MM-DDThh]`` for usage ending
            **before** this hour.
        :type end_hr: datetime, optional
        :rtype: UsageDBMResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["start_hr"] = start_hr

        if end_hr is not unset:
            kwargs["end_hr"] = end_hr

        return self._get_usage_dbm_endpoint.call_with_http_info(**kwargs)

    def get_usage_fargate(
        self,
        start_hr: datetime,
        *,
        end_hr: Union[datetime, UnsetType] = unset,
    ) -> UsageFargateResponse:
        """Get hourly usage for Fargate.

        Get hourly usage for `Fargate <https://docs.datadoghq.com/integrations/ecs_fargate/>`_.
        **Note:** hourly usage data for all products is now available in the `Get hourly usage by product family API <https://docs.datadoghq.com/api/latest/usage-metering/#get-hourly-usage-by-product-family>`_. Refer to `Migrating from the V1 Hourly Usage APIs to V2 <https://docs.datadoghq.com/account_management/guide/hourly-usage-migration/>`_ for the associated migration guide.

        :param start_hr: Datetime in ISO-8601 format, UTC, precise to hour: [YYYY-MM-DDThh] for usage beginning at this hour.
        :type start_hr: datetime
        :param end_hr: Datetime in ISO-8601 format, UTC, precise to hour: [YYYY-MM-DDThh] for usage ending **before** this hour.
        :type end_hr: datetime, optional
        :rtype: UsageFargateResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["start_hr"] = start_hr

        if end_hr is not unset:
            kwargs["end_hr"] = end_hr

        return self._get_usage_fargate_endpoint.call_with_http_info(**kwargs)

    def get_usage_hosts(
        self,
        start_hr: datetime,
        *,
        end_hr: Union[datetime, UnsetType] = unset,
    ) -> UsageHostsResponse:
        """Get hourly usage for hosts and containers.

        Get hourly usage for hosts and containers.
        **Note:** hourly usage data for all products is now available in the `Get hourly usage by product family API <https://docs.datadoghq.com/api/latest/usage-metering/#get-hourly-usage-by-product-family>`_. Refer to `Migrating from the V1 Hourly Usage APIs to V2 <https://docs.datadoghq.com/account_management/guide/hourly-usage-migration/>`_ for the associated migration guide.

        :param start_hr: Datetime in ISO-8601 format, UTC, precise to hour: [YYYY-MM-DDThh] for usage beginning at this hour.
        :type start_hr: datetime
        :param end_hr: Datetime in ISO-8601 format, UTC, precise to hour: [YYYY-MM-DDThh] for usage ending **before** this hour.
        :type end_hr: datetime, optional
        :rtype: UsageHostsResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["start_hr"] = start_hr

        if end_hr is not unset:
            kwargs["end_hr"] = end_hr

        return self._get_usage_hosts_endpoint.call_with_http_info(**kwargs)

    def get_usage_indexed_spans(
        self,
        start_hr: datetime,
        *,
        end_hr: Union[datetime, UnsetType] = unset,
    ) -> UsageIndexedSpansResponse:
        """Get hourly usage for indexed spans.

        Get hourly usage for indexed spans.
        **Note:** hourly usage data for all products is now available in the `Get hourly usage by product family API <https://docs.datadoghq.com/api/latest/usage-metering/#get-hourly-usage-by-product-family>`_. Refer to `Migrating from the V1 Hourly Usage APIs to V2 <https://docs.datadoghq.com/account_management/guide/hourly-usage-migration/>`_ for the associated migration guide.

        :param start_hr: Datetime in ISO-8601 format, UTC, precise to hour: ``[YYYY-MM-DDThh]`` for usage beginning at this hour.
        :type start_hr: datetime
        :param end_hr: Datetime in ISO-8601 format, UTC, precise to hour: ``[YYYY-MM-DDThh]`` for usage ending **before** this hour.
        :type end_hr: datetime, optional
        :rtype: UsageIndexedSpansResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["start_hr"] = start_hr

        if end_hr is not unset:
            kwargs["end_hr"] = end_hr

        return self._get_usage_indexed_spans_endpoint.call_with_http_info(**kwargs)

    def get_usage_internet_of_things(
        self,
        start_hr: datetime,
        *,
        end_hr: Union[datetime, UnsetType] = unset,
    ) -> UsageIoTResponse:
        """Get hourly usage for IoT.

        Get hourly usage for IoT.
        **Note:** hourly usage data for all products is now available in the `Get hourly usage by product family API <https://docs.datadoghq.com/api/latest/usage-metering/#get-hourly-usage-by-product-family>`_. Refer to `Migrating from the V1 Hourly Usage APIs to V2 <https://docs.datadoghq.com/account_management/guide/hourly-usage-migration/>`_ for the associated migration guide.

        :param start_hr: Datetime in ISO-8601 format, UTC, precise to hour: ``[YYYY-MM-DDThh]`` for usage beginning at this hour.
        :type start_hr: datetime
        :param end_hr: Datetime in ISO-8601 format, UTC, precise to hour: ``[YYYY-MM-DDThh]`` for usage ending
            **before** this hour.
        :type end_hr: datetime, optional
        :rtype: UsageIoTResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["start_hr"] = start_hr

        if end_hr is not unset:
            kwargs["end_hr"] = end_hr

        return self._get_usage_internet_of_things_endpoint.call_with_http_info(**kwargs)

    def get_usage_lambda(
        self,
        start_hr: datetime,
        *,
        end_hr: Union[datetime, UnsetType] = unset,
    ) -> UsageLambdaResponse:
        """Get hourly usage for lambda.

        Get hourly usage for lambda.
        **Note:** hourly usage data for all products is now available in the `Get hourly usage by product family API <https://docs.datadoghq.com/api/latest/usage-metering/#get-hourly-usage-by-product-family>`_. Refer to `Migrating from the V1 Hourly Usage APIs to V2 <https://docs.datadoghq.com/account_management/guide/hourly-usage-migration/>`_ for the associated migration guide.

        :param start_hr: Datetime in ISO-8601 format, UTC, precise to hour: [YYYY-MM-DDThh] for usage beginning at this hour.
        :type start_hr: datetime
        :param end_hr: Datetime in ISO-8601 format, UTC, precise to hour: [YYYY-MM-DDThh] for usage ending **before** this hour.
        :type end_hr: datetime, optional
        :rtype: UsageLambdaResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["start_hr"] = start_hr

        if end_hr is not unset:
            kwargs["end_hr"] = end_hr

        return self._get_usage_lambda_endpoint.call_with_http_info(**kwargs)

    def get_usage_logs(
        self,
        start_hr: datetime,
        *,
        end_hr: Union[datetime, UnsetType] = unset,
    ) -> UsageLogsResponse:
        """Get hourly usage for logs.

        Get hourly usage for logs.
        **Note:** hourly usage data for all products is now available in the `Get hourly usage by product family API <https://docs.datadoghq.com/api/latest/usage-metering/#get-hourly-usage-by-product-family>`_. Refer to `Migrating from the V1 Hourly Usage APIs to V2 <https://docs.datadoghq.com/account_management/guide/hourly-usage-migration/>`_ for the associated migration guide.

        :param start_hr: Datetime in ISO-8601 format, UTC, precise to hour: [YYYY-MM-DDThh] for usage beginning at this hour.
        :type start_hr: datetime
        :param end_hr: Datetime in ISO-8601 format, UTC, precise to hour: [YYYY-MM-DDThh] for usage ending **before** this hour.
        :type end_hr: datetime, optional
        :rtype: UsageLogsResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["start_hr"] = start_hr

        if end_hr is not unset:
            kwargs["end_hr"] = end_hr

        return self._get_usage_logs_endpoint.call_with_http_info(**kwargs)

    def get_usage_logs_by_index(
        self,
        start_hr: datetime,
        *,
        end_hr: Union[datetime, UnsetType] = unset,
        index_name: Union[List[str], UnsetType] = unset,
    ) -> UsageLogsByIndexResponse:
        """Get hourly usage for logs by index.

        Get hourly usage for logs by index.

        :param start_hr: Datetime in ISO-8601 format, UTC, precise to hour: [YYYY-MM-DDThh] for usage beginning at this hour.
        :type start_hr: datetime
        :param end_hr: Datetime in ISO-8601 format, UTC, precise to hour: [YYYY-MM-DDThh] for usage ending **before** this hour.
        :type end_hr: datetime, optional
        :param index_name: Comma-separated list of log index names.
        :type index_name: [str], optional
        :rtype: UsageLogsByIndexResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["start_hr"] = start_hr

        if end_hr is not unset:
            kwargs["end_hr"] = end_hr

        if index_name is not unset:
            kwargs["index_name"] = index_name

        return self._get_usage_logs_by_index_endpoint.call_with_http_info(**kwargs)

    def get_usage_logs_by_retention(
        self,
        start_hr: datetime,
        *,
        end_hr: Union[datetime, UnsetType] = unset,
    ) -> UsageLogsByRetentionResponse:
        """Get hourly logs usage by retention.

        Get hourly usage for indexed logs by retention period.
        **Note:** hourly usage data for all products is now available in the `Get hourly usage by product family API <https://docs.datadoghq.com/api/latest/usage-metering/#get-hourly-usage-by-product-family>`_. Refer to `Migrating from the V1 Hourly Usage APIs to V2 <https://docs.datadoghq.com/account_management/guide/hourly-usage-migration/>`_ for the associated migration guide.

        :param start_hr: Datetime in ISO-8601 format, UTC, precise to hour: ``[YYYY-MM-DDThh]`` for usage beginning at this hour.
        :type start_hr: datetime
        :param end_hr: Datetime in ISO-8601 format, UTC, precise to hour: ``[YYYY-MM-DDThh]`` for usage ending
            **before** this hour.
        :type end_hr: datetime, optional
        :rtype: UsageLogsByRetentionResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["start_hr"] = start_hr

        if end_hr is not unset:
            kwargs["end_hr"] = end_hr

        return self._get_usage_logs_by_retention_endpoint.call_with_http_info(**kwargs)

    def get_usage_network_flows(
        self,
        start_hr: datetime,
        *,
        end_hr: Union[datetime, UnsetType] = unset,
    ) -> UsageNetworkFlowsResponse:
        """get hourly usage for network flows.

        Get hourly usage for network flows.
        **Note:** hourly usage data for all products is now available in the `Get hourly usage by product family API <https://docs.datadoghq.com/api/latest/usage-metering/#get-hourly-usage-by-product-family>`_. Refer to `Migrating from the V1 Hourly Usage APIs to V2 <https://docs.datadoghq.com/account_management/guide/hourly-usage-migration/>`_ for the associated migration guide.

        :param start_hr: Datetime in ISO-8601 format, UTC, precise to hour: ``[YYYY-MM-DDThh]`` for usage beginning at this hour.
        :type start_hr: datetime
        :param end_hr: Datetime in ISO-8601 format, UTC, precise to hour: ``[YYYY-MM-DDThh]`` for usage ending
            **before** this hour.
        :type end_hr: datetime, optional
        :rtype: UsageNetworkFlowsResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["start_hr"] = start_hr

        if end_hr is not unset:
            kwargs["end_hr"] = end_hr

        return self._get_usage_network_flows_endpoint.call_with_http_info(**kwargs)

    def get_usage_network_hosts(
        self,
        start_hr: datetime,
        *,
        end_hr: Union[datetime, UnsetType] = unset,
    ) -> UsageNetworkHostsResponse:
        """Get hourly usage for network hosts.

        Get hourly usage for network hosts.
        **Note:** hourly usage data for all products is now available in the `Get hourly usage by product family API <https://docs.datadoghq.com/api/latest/usage-metering/#get-hourly-usage-by-product-family>`_. Refer to `Migrating from the V1 Hourly Usage APIs to V2 <https://docs.datadoghq.com/account_management/guide/hourly-usage-migration/>`_ for the associated migration guide.

        :param start_hr: Datetime in ISO-8601 format, UTC, precise to hour: [YYYY-MM-DDThh] for usage beginning at this hour.
        :type start_hr: datetime
        :param end_hr: Datetime in ISO-8601 format, UTC, precise to hour: [YYYY-MM-DDThh] for usage ending **before** this hour.
        :type end_hr: datetime, optional
        :rtype: UsageNetworkHostsResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["start_hr"] = start_hr

        if end_hr is not unset:
            kwargs["end_hr"] = end_hr

        return self._get_usage_network_hosts_endpoint.call_with_http_info(**kwargs)

    def get_usage_online_archive(
        self,
        start_hr: datetime,
        *,
        end_hr: Union[datetime, UnsetType] = unset,
    ) -> UsageOnlineArchiveResponse:
        """Get hourly usage for online archive.

        Get hourly usage for online archive.
        **Note:** hourly usage data for all products is now available in the `Get hourly usage by product family API <https://docs.datadoghq.com/api/latest/usage-metering/#get-hourly-usage-by-product-family>`_. Refer to `Migrating from the V1 Hourly Usage APIs to V2 <https://docs.datadoghq.com/account_management/guide/hourly-usage-migration/>`_ for the associated migration guide.

        :param start_hr: Datetime in ISO-8601 format, UTC, precise to hour: ``[YYYY-MM-DDThh]`` for usage beginning at this hour.
        :type start_hr: datetime
        :param end_hr: Datetime in ISO-8601 format, UTC, precise to hour: ``[YYYY-MM-DDThh]`` for usage ending
            **before** this hour.
        :type end_hr: datetime, optional
        :rtype: UsageOnlineArchiveResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["start_hr"] = start_hr

        if end_hr is not unset:
            kwargs["end_hr"] = end_hr

        return self._get_usage_online_archive_endpoint.call_with_http_info(**kwargs)

    def get_usage_profiling(
        self,
        start_hr: datetime,
        *,
        end_hr: Union[datetime, UnsetType] = unset,
    ) -> UsageProfilingResponse:
        """Get hourly usage for profiled hosts.

        Get hourly usage for profiled hosts.
        **Note:** hourly usage data for all products is now available in the `Get hourly usage by product family API <https://docs.datadoghq.com/api/latest/usage-metering/#get-hourly-usage-by-product-family>`_. Refer to `Migrating from the V1 Hourly Usage APIs to V2 <https://docs.datadoghq.com/account_management/guide/hourly-usage-migration/>`_ for the associated migration guide.

        :param start_hr: Datetime in ISO-8601 format, UTC, precise to hour: ``[YYYY-MM-DDThh]`` for usage beginning at this hour.
        :type start_hr: datetime
        :param end_hr: Datetime in ISO-8601 format, UTC, precise to hour: ``[YYYY-MM-DDThh]`` for usage ending
            **before** this hour.
        :type end_hr: datetime, optional
        :rtype: UsageProfilingResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["start_hr"] = start_hr

        if end_hr is not unset:
            kwargs["end_hr"] = end_hr

        return self._get_usage_profiling_endpoint.call_with_http_info(**kwargs)

    def get_usage_rum_sessions(
        self,
        start_hr: datetime,
        *,
        end_hr: Union[datetime, UnsetType] = unset,
        type: Union[str, UnsetType] = unset,
    ) -> UsageRumSessionsResponse:
        """Get hourly usage for RUM sessions.

        Get hourly usage for `RUM <https://docs.datadoghq.com/real_user_monitoring/>`_ Sessions.
        **Note:** hourly usage data for all products is now available in the `Get hourly usage by product family API <https://docs.datadoghq.com/api/latest/usage-metering/#get-hourly-usage-by-product-family>`_. Refer to `Migrating from the V1 Hourly Usage APIs to V2 <https://docs.datadoghq.com/account_management/guide/hourly-usage-migration/>`_ for the associated migration guide.

        :param start_hr: Datetime in ISO-8601 format, UTC, precise to hour: [YYYY-MM-DDThh] for usage beginning at this hour.
        :type start_hr: datetime
        :param end_hr: Datetime in ISO-8601 format, UTC, precise to hour: [YYYY-MM-DDThh] for usage ending **before** this hour.
        :type end_hr: datetime, optional
        :param type: RUM type: ``[browser, mobile]``. Defaults to ``browser``.
        :type type: str, optional
        :rtype: UsageRumSessionsResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["start_hr"] = start_hr

        if end_hr is not unset:
            kwargs["end_hr"] = end_hr

        if type is not unset:
            kwargs["type"] = type

        return self._get_usage_rum_sessions_endpoint.call_with_http_info(**kwargs)

    def get_usage_rum_units(
        self,
        start_hr: datetime,
        *,
        end_hr: Union[datetime, UnsetType] = unset,
    ) -> UsageRumUnitsResponse:
        """Get hourly usage for RUM units.

        Get hourly usage for `RUM <https://docs.datadoghq.com/real_user_monitoring/>`_ Units.
        **Note:** hourly usage data for all products is now available in the `Get hourly usage by product family API <https://docs.datadoghq.com/api/latest/usage-metering/#get-hourly-usage-by-product-family>`_. Refer to `Migrating from the V1 Hourly Usage APIs to V2 <https://docs.datadoghq.com/account_management/guide/hourly-usage-migration/>`_ for the associated migration guide.

        :param start_hr: Datetime in ISO-8601 format, UTC, precise to hour: [YYYY-MM-DDThh] for usage beginning at this hour.
        :type start_hr: datetime
        :param end_hr: Datetime in ISO-8601 format, UTC, precise to hour: [YYYY-MM-DDThh] for usage ending **before** this hour.
        :type end_hr: datetime, optional
        :rtype: UsageRumUnitsResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["start_hr"] = start_hr

        if end_hr is not unset:
            kwargs["end_hr"] = end_hr

        return self._get_usage_rum_units_endpoint.call_with_http_info(**kwargs)

    def get_usage_sds(
        self,
        start_hr: datetime,
        *,
        end_hr: Union[datetime, UnsetType] = unset,
    ) -> UsageSDSResponse:
        """Get hourly usage for sensitive data scanner.

        Get hourly usage for sensitive data scanner.
        **Note:** hourly usage data for all products is now available in the `Get hourly usage by product family API <https://docs.datadoghq.com/api/latest/usage-metering/#get-hourly-usage-by-product-family>`_. Refer to `Migrating from the V1 Hourly Usage APIs to V2 <https://docs.datadoghq.com/account_management/guide/hourly-usage-migration/>`_ for the associated migration guide.

        :param start_hr: Datetime in ISO-8601 format, UTC, precise to hour: ``[YYYY-MM-DDThh]`` for usage beginning at this hour.
        :type start_hr: datetime
        :param end_hr: Datetime in ISO-8601 format, UTC, precise to hour: ``[YYYY-MM-DDThh]`` for usage ending
            **before** this hour.
        :type end_hr: datetime, optional
        :rtype: UsageSDSResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["start_hr"] = start_hr

        if end_hr is not unset:
            kwargs["end_hr"] = end_hr

        return self._get_usage_sds_endpoint.call_with_http_info(**kwargs)

    def get_usage_snmp(
        self,
        start_hr: datetime,
        *,
        end_hr: Union[datetime, UnsetType] = unset,
    ) -> UsageSNMPResponse:
        """Get hourly usage for SNMP devices.

        Get hourly usage for SNMP devices.
        **Note:** hourly usage data for all products is now available in the `Get hourly usage by product family API <https://docs.datadoghq.com/api/latest/usage-metering/#get-hourly-usage-by-product-family>`_. Refer to `Migrating from the V1 Hourly Usage APIs to V2 <https://docs.datadoghq.com/account_management/guide/hourly-usage-migration/>`_ for the associated migration guide.

        :param start_hr: Datetime in ISO-8601 format, UTC, precise to hour: ``[YYYY-MM-DDThh]`` for usage beginning at this hour.
        :type start_hr: datetime
        :param end_hr: Datetime in ISO-8601 format, UTC, precise to hour: ``[YYYY-MM-DDThh]`` for usage ending
            **before** this hour.
        :type end_hr: datetime, optional
        :rtype: UsageSNMPResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["start_hr"] = start_hr

        if end_hr is not unset:
            kwargs["end_hr"] = end_hr

        return self._get_usage_snmp_endpoint.call_with_http_info(**kwargs)

    def get_usage_summary(
        self,
        start_month: datetime,
        *,
        end_month: Union[datetime, UnsetType] = unset,
        include_org_details: Union[bool, UnsetType] = unset,
    ) -> UsageSummaryResponse:
        """Get usage across your account.

        Get all usage across your account.

        :param start_month: Datetime in ISO-8601 format, UTC, precise to month: ``[YYYY-MM]`` for usage beginning in this month.
            Maximum of 15 months ago.
        :type start_month: datetime
        :param end_month: Datetime in ISO-8601 format, UTC, precise to month: ``[YYYY-MM]`` for usage ending this month.
        :type end_month: datetime, optional
        :param include_org_details: Include usage summaries for each sub-org.
        :type include_org_details: bool, optional
        :rtype: UsageSummaryResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["start_month"] = start_month

        if end_month is not unset:
            kwargs["end_month"] = end_month

        if include_org_details is not unset:
            kwargs["include_org_details"] = include_org_details

        return self._get_usage_summary_endpoint.call_with_http_info(**kwargs)

    def get_usage_synthetics(
        self,
        start_hr: datetime,
        *,
        end_hr: Union[datetime, UnsetType] = unset,
    ) -> UsageSyntheticsResponse:
        """Get hourly usage for synthetics checks. **Deprecated**.

        Get hourly usage for `synthetics checks <https://docs.datadoghq.com/synthetics/>`_.
        **Note:** hourly usage data for all products is now available in the `Get hourly usage by product family API <https://docs.datadoghq.com/api/latest/usage-metering/#get-hourly-usage-by-product-family>`_. Refer to `Migrating from the V1 Hourly Usage APIs to V2 <https://docs.datadoghq.com/account_management/guide/hourly-usage-migration/>`_ for the associated migration guide.

        :param start_hr: Datetime in ISO-8601 format, UTC, precise to hour: [YYYY-MM-DDThh] for usage beginning at this hour.
        :type start_hr: datetime
        :param end_hr: Datetime in ISO-8601 format, UTC, precise to hour: [YYYY-MM-DDThh] for usage ending **before** this hour.
        :type end_hr: datetime, optional
        :rtype: UsageSyntheticsResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["start_hr"] = start_hr

        if end_hr is not unset:
            kwargs["end_hr"] = end_hr

        warnings.warn("get_usage_synthetics is deprecated", DeprecationWarning, stacklevel=2)
        return self._get_usage_synthetics_endpoint.call_with_http_info(**kwargs)

    def get_usage_synthetics_api(
        self,
        start_hr: datetime,
        *,
        end_hr: Union[datetime, UnsetType] = unset,
    ) -> UsageSyntheticsAPIResponse:
        """Get hourly usage for synthetics API checks.

        Get hourly usage for `synthetics API checks <https://docs.datadoghq.com/synthetics/>`_.
        **Note:** hourly usage data for all products is now available in the `Get hourly usage by product family API <https://docs.datadoghq.com/api/latest/usage-metering/#get-hourly-usage-by-product-family>`_. Refer to `Migrating from the V1 Hourly Usage APIs to V2 <https://docs.datadoghq.com/account_management/guide/hourly-usage-migration/>`_ for the associated migration guide.

        :param start_hr: Datetime in ISO-8601 format, UTC, precise to hour: [YYYY-MM-DDThh] for usage beginning at this hour.
        :type start_hr: datetime
        :param end_hr: Datetime in ISO-8601 format, UTC, precise to hour: [YYYY-MM-DDThh] for usage ending **before** this hour.
        :type end_hr: datetime, optional
        :rtype: UsageSyntheticsAPIResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["start_hr"] = start_hr

        if end_hr is not unset:
            kwargs["end_hr"] = end_hr

        return self._get_usage_synthetics_api_endpoint.call_with_http_info(**kwargs)

    def get_usage_synthetics_browser(
        self,
        start_hr: datetime,
        *,
        end_hr: Union[datetime, UnsetType] = unset,
    ) -> UsageSyntheticsBrowserResponse:
        """Get hourly usage for synthetics browser checks.

        Get hourly usage for synthetics browser checks.
        **Note:** hourly usage data for all products is now available in the `Get hourly usage by product family API <https://docs.datadoghq.com/api/latest/usage-metering/#get-hourly-usage-by-product-family>`_. Refer to `Migrating from the V1 Hourly Usage APIs to V2 <https://docs.datadoghq.com/account_management/guide/hourly-usage-migration/>`_ for the associated migration guide.

        :param start_hr: Datetime in ISO-8601 format, UTC, precise to hour: [YYYY-MM-DDThh] for usage beginning at this hour.
        :type start_hr: datetime
        :param end_hr: Datetime in ISO-8601 format, UTC, precise to hour: [YYYY-MM-DDThh] for usage ending **before** this hour.
        :type end_hr: datetime, optional
        :rtype: UsageSyntheticsBrowserResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["start_hr"] = start_hr

        if end_hr is not unset:
            kwargs["end_hr"] = end_hr

        return self._get_usage_synthetics_browser_endpoint.call_with_http_info(**kwargs)

    def get_usage_timeseries(
        self,
        start_hr: datetime,
        *,
        end_hr: Union[datetime, UnsetType] = unset,
    ) -> UsageTimeseriesResponse:
        """Get hourly usage for custom metrics.

        Get hourly usage for `custom metrics <https://docs.datadoghq.com/developers/metrics/custom_metrics/>`_.
        **Note:** hourly usage data for all products is now available in the `Get hourly usage by product family API <https://docs.datadoghq.com/api/latest/usage-metering/#get-hourly-usage-by-product-family>`_. Refer to `Migrating from the V1 Hourly Usage APIs to V2 <https://docs.datadoghq.com/account_management/guide/hourly-usage-migration/>`_ for the associated migration guide.

        :param start_hr: Datetime in ISO-8601 format, UTC, precise to hour: [YYYY-MM-DDThh] for usage beginning at this hour.
        :type start_hr: datetime
        :param end_hr: Datetime in ISO-8601 format, UTC, precise to hour: [YYYY-MM-DDThh] for usage ending **before** this hour.
        :type end_hr: datetime, optional
        :rtype: UsageTimeseriesResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["start_hr"] = start_hr

        if end_hr is not unset:
            kwargs["end_hr"] = end_hr

        return self._get_usage_timeseries_endpoint.call_with_http_info(**kwargs)

    def get_usage_top_avg_metrics(
        self,
        *,
        month: Union[datetime, UnsetType] = unset,
        day: Union[datetime, UnsetType] = unset,
        names: Union[List[str], UnsetType] = unset,
        limit: Union[int, UnsetType] = unset,
        next_record_id: Union[str, UnsetType] = unset,
    ) -> UsageTopAvgMetricsResponse:
        """Get all custom metrics by hourly average.

        Get all `custom metrics <https://docs.datadoghq.com/developers/metrics/custom_metrics/>`_ by hourly average. Use the month parameter to get a month-to-date data resolution or use the day parameter to get a daily resolution. One of the two is required, and only one of the two is allowed.

        :param month: Datetime in ISO-8601 format, UTC, precise to month: [YYYY-MM] for usage beginning at this hour. (Either month or day should be specified, but not both)
        :type month: datetime, optional
        :param day: Datetime in ISO-8601 format, UTC, precise to day: [YYYY-MM-DD] for usage beginning at this hour. (Either month or day should be specified, but not both)
        :type day: datetime, optional
        :param names: Comma-separated list of metric names.
        :type names: [str], optional
        :param limit: Maximum number of results to return (between 1 and 5000) - defaults to 500 results if limit not specified.
        :type limit: int, optional
        :param next_record_id: List following results with a next_record_id provided in the previous query.
        :type next_record_id: str, optional
        :rtype: UsageTopAvgMetricsResponse
        """
        kwargs: Dict[str, Any] = {}
        if month is not unset:
            kwargs["month"] = month

        if day is not unset:
            kwargs["day"] = day

        if names is not unset:
            kwargs["names"] = names

        if limit is not unset:
            kwargs["limit"] = limit

        if next_record_id is not unset:
            kwargs["next_record_id"] = next_record_id

        return self._get_usage_top_avg_metrics_endpoint.call_with_http_info(**kwargs)
