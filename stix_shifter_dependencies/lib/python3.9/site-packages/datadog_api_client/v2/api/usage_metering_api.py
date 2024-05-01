# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Any, Dict, Union
import warnings

from datadog_api_client.api_client import ApiClient, Endpoint as _Endpoint
from datadog_api_client.configuration import Configuration
from datadog_api_client.model_utils import (
    datetime,
    UnsetType,
    unset,
)
from datadog_api_client.v2.model.usage_application_security_monitoring_response import (
    UsageApplicationSecurityMonitoringResponse,
)
from datadog_api_client.v2.model.cost_by_org_response import CostByOrgResponse
from datadog_api_client.v2.model.hourly_usage_response import HourlyUsageResponse
from datadog_api_client.v2.model.usage_lambda_traced_invocations_response import UsageLambdaTracedInvocationsResponse
from datadog_api_client.v2.model.usage_observability_pipelines_response import UsageObservabilityPipelinesResponse


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

        self._get_cost_by_org_endpoint = _Endpoint(
            settings={
                "response_type": (CostByOrgResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v2/usage/cost_by_org",
                "operation_id": "get_cost_by_org",
                "http_method": "GET",
                "version": "v2",
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
            },
            headers_map={
                "accept": ["application/json;datetime-format=rfc3339"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._get_estimated_cost_by_org_endpoint = _Endpoint(
            settings={
                "response_type": (CostByOrgResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v2/usage/estimated_cost",
                "operation_id": "get_estimated_cost_by_org",
                "http_method": "GET",
                "version": "v2",
                "servers": None,
            },
            params_map={
                "view": {
                    "openapi_types": (str,),
                    "attribute": "view",
                    "location": "query",
                },
                "start_month": {
                    "openapi_types": (datetime,),
                    "attribute": "start_month",
                    "location": "query",
                },
                "end_month": {
                    "openapi_types": (datetime,),
                    "attribute": "end_month",
                    "location": "query",
                },
                "start_date": {
                    "openapi_types": (datetime,),
                    "attribute": "start_date",
                    "location": "query",
                },
                "end_date": {
                    "openapi_types": (datetime,),
                    "attribute": "end_date",
                    "location": "query",
                },
            },
            headers_map={
                "accept": ["application/json;datetime-format=rfc3339"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._get_historical_cost_by_org_endpoint = _Endpoint(
            settings={
                "response_type": (CostByOrgResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v2/usage/historical_cost",
                "operation_id": "get_historical_cost_by_org",
                "http_method": "GET",
                "version": "v2",
                "servers": None,
            },
            params_map={
                "view": {
                    "openapi_types": (str,),
                    "attribute": "view",
                    "location": "query",
                },
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
            },
            headers_map={
                "accept": ["application/json;datetime-format=rfc3339"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._get_hourly_usage_endpoint = _Endpoint(
            settings={
                "response_type": (HourlyUsageResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v2/usage/hourly_usage",
                "operation_id": "get_hourly_usage",
                "http_method": "GET",
                "version": "v2",
                "servers": None,
            },
            params_map={
                "filter_timestamp_start": {
                    "required": True,
                    "openapi_types": (datetime,),
                    "attribute": "filter[timestamp][start]",
                    "location": "query",
                },
                "filter_timestamp_end": {
                    "openapi_types": (datetime,),
                    "attribute": "filter[timestamp][end]",
                    "location": "query",
                },
                "filter_product_families": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "filter[product_families]",
                    "location": "query",
                },
                "filter_include_descendants": {
                    "openapi_types": (bool,),
                    "attribute": "filter[include_descendants]",
                    "location": "query",
                },
                "filter_versions": {
                    "openapi_types": (str,),
                    "attribute": "filter[versions]",
                    "location": "query",
                },
                "page_limit": {
                    "validation": {
                        "inclusive_maximum": 500,
                        "inclusive_minimum": 1,
                    },
                    "openapi_types": (int,),
                    "attribute": "page[limit]",
                    "location": "query",
                },
                "page_next_record_id": {
                    "openapi_types": (str,),
                    "attribute": "page[next_record_id]",
                    "location": "query",
                },
            },
            headers_map={
                "accept": ["application/json;datetime-format=rfc3339"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._get_usage_application_security_monitoring_endpoint = _Endpoint(
            settings={
                "response_type": (UsageApplicationSecurityMonitoringResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v2/usage/application_security",
                "operation_id": "get_usage_application_security_monitoring",
                "http_method": "GET",
                "version": "v2",
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

        self._get_usage_lambda_traced_invocations_endpoint = _Endpoint(
            settings={
                "response_type": (UsageLambdaTracedInvocationsResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v2/usage/lambda_traced_invocations",
                "operation_id": "get_usage_lambda_traced_invocations",
                "http_method": "GET",
                "version": "v2",
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

        self._get_usage_observability_pipelines_endpoint = _Endpoint(
            settings={
                "response_type": (UsageObservabilityPipelinesResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v2/usage/observability_pipelines",
                "operation_id": "get_usage_observability_pipelines",
                "http_method": "GET",
                "version": "v2",
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

    def get_cost_by_org(
        self,
        start_month: datetime,
        *,
        end_month: Union[datetime, UnsetType] = unset,
    ) -> CostByOrgResponse:
        """Get cost across multi-org account. **Deprecated**.

        Get cost across multi-org account.
        Cost by org data for a given month becomes available no later than the 16th of the following month.
        **Note:** This endpoint has been deprecated. Please use the new endpoint
        ` ``/historical_cost`` <https://docs.datadoghq.com/api/latest/usage-metering/#get-historical-cost-across-your-account>`_
        instead.

        :param start_month: Datetime in ISO-8601 format, UTC, precise to month: ``[YYYY-MM]`` for cost beginning this month.
        :type start_month: datetime
        :param end_month: Datetime in ISO-8601 format, UTC, precise to month: ``[YYYY-MM]`` for cost ending this month.
        :type end_month: datetime, optional
        :rtype: CostByOrgResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["start_month"] = start_month

        if end_month is not unset:
            kwargs["end_month"] = end_month

        warnings.warn("get_cost_by_org is deprecated", DeprecationWarning, stacklevel=2)
        return self._get_cost_by_org_endpoint.call_with_http_info(**kwargs)

    def get_estimated_cost_by_org(
        self,
        *,
        view: Union[str, UnsetType] = unset,
        start_month: Union[datetime, UnsetType] = unset,
        end_month: Union[datetime, UnsetType] = unset,
        start_date: Union[datetime, UnsetType] = unset,
        end_date: Union[datetime, UnsetType] = unset,
    ) -> CostByOrgResponse:
        """Get estimated cost across your account.

        Get estimated cost across multi-org and single root-org accounts.
        Estimated cost data is only available for the current month and previous month
        and is delayed by up to 72 hours from when it was incurred.
        To access historical costs prior to this, use the ``/historical_cost`` endpoint.

        :param view: String to specify whether cost is broken down at a parent-org level or at the sub-org level. Available views are ``summary`` and ``sub-org``. Defaults to ``summary``.
        :type view: str, optional
        :param start_month: Datetime in ISO-8601 format, UTC, precise to month: ``[YYYY-MM]`` for cost beginning this month. Either start_month or start_date should be specified, but not both. (start_month cannot go beyond two months in the past)
        :type start_month: datetime, optional
        :param end_month: Datetime in ISO-8601 format, UTC, precise to month: ``[YYYY-MM]`` for cost ending this month.
        :type end_month: datetime, optional
        :param start_date: Datetime in ISO-8601 format, UTC, precise to day: ``[YYYY-MM-DD]`` for cost beginning this day. Either start_month or start_date should be specified, but not both. (start_date cannot go beyond two months in the past)
        :type start_date: datetime, optional
        :param end_date: Datetime in ISO-8601 format, UTC, precise to day: ``[YYYY-MM-DD]`` for cost ending this day.
        :type end_date: datetime, optional
        :rtype: CostByOrgResponse
        """
        kwargs: Dict[str, Any] = {}
        if view is not unset:
            kwargs["view"] = view

        if start_month is not unset:
            kwargs["start_month"] = start_month

        if end_month is not unset:
            kwargs["end_month"] = end_month

        if start_date is not unset:
            kwargs["start_date"] = start_date

        if end_date is not unset:
            kwargs["end_date"] = end_date

        return self._get_estimated_cost_by_org_endpoint.call_with_http_info(**kwargs)

    def get_historical_cost_by_org(
        self,
        start_month: datetime,
        *,
        view: Union[str, UnsetType] = unset,
        end_month: Union[datetime, UnsetType] = unset,
    ) -> CostByOrgResponse:
        """Get historical cost across your account.

        Get historical cost across multi-org and single root-org accounts.
        Cost data for a given month becomes available no later than the 16th of the following month.

        :param start_month: Datetime in ISO-8601 format, UTC, precise to month: ``[YYYY-MM]`` for cost beginning this month.
        :type start_month: datetime
        :param view: String to specify whether cost is broken down at a parent-org level or at the sub-org level. Available views are ``summary`` and ``sub-org``.  Defaults to ``summary``.
        :type view: str, optional
        :param end_month: Datetime in ISO-8601 format, UTC, precise to month: ``[YYYY-MM]`` for cost ending this month.
        :type end_month: datetime, optional
        :rtype: CostByOrgResponse
        """
        kwargs: Dict[str, Any] = {}
        if view is not unset:
            kwargs["view"] = view

        kwargs["start_month"] = start_month

        if end_month is not unset:
            kwargs["end_month"] = end_month

        return self._get_historical_cost_by_org_endpoint.call_with_http_info(**kwargs)

    def get_hourly_usage(
        self,
        filter_timestamp_start: datetime,
        filter_product_families: str,
        *,
        filter_timestamp_end: Union[datetime, UnsetType] = unset,
        filter_include_descendants: Union[bool, UnsetType] = unset,
        filter_versions: Union[str, UnsetType] = unset,
        page_limit: Union[int, UnsetType] = unset,
        page_next_record_id: Union[str, UnsetType] = unset,
    ) -> HourlyUsageResponse:
        """Get hourly usage by product family.

        Get hourly usage by product family.

        :param filter_timestamp_start: Datetime in ISO-8601 format, UTC, precise to hour: [YYYY-MM-DDThh] for usage beginning at this hour.
        :type filter_timestamp_start: datetime
        :param filter_product_families: Comma separated list of product families to retrieve. Available families are ``all`` , ``analyzed_logs`` ,
            ``application_security`` , ``audit_trail`` , ``serverless`` , ``ci_app`` , ``cloud_cost_management`` ,
            ``cspm`` , ``custom_events`` , ``cws`` , ``dbm`` , ``fargate`` ,
            ``infra_hosts`` , ``incident_management`` , ``indexed_logs`` , ``indexed_spans`` , ``ingested_spans`` , ``iot`` ,
            ``lambda_traced_invocations`` , ``logs`` , ``network_flows`` , ``network_hosts`` , ``observability_pipelines`` ,
            ``online_archive`` , ``profiling`` , ``rum`` , ``rum_browser_sessions`` , ``rum_mobile_sessions`` , ``sds`` , ``snmp`` ,
            ``synthetics_api`` , ``synthetics_browser`` , ``synthetics_parallel_testing`` , and ``timeseries``.
            The following product family has been **deprecated** : ``audit_logs``.
        :type filter_product_families: str
        :param filter_timestamp_end: Datetime in ISO-8601 format, UTC, precise to hour: [YYYY-MM-DDThh] for usage ending **before** this hour.
        :type filter_timestamp_end: datetime, optional
        :param filter_include_descendants: Include child org usage in the response. Defaults to false.
        :type filter_include_descendants: bool, optional
        :param filter_versions: Comma separated list of product family versions to use in the format ``product_family:version``. For example,
            ``infra_hosts:1.0.0``. If this parameter is not used, the API will use the latest version of each requested
            product family. Currently all families have one version ``1.0.0``.
        :type filter_versions: str, optional
        :param page_limit: Maximum number of results to return (between 1 and 500) - defaults to 500 if limit not specified.
        :type page_limit: int, optional
        :param page_next_record_id: List following results with a next_record_id provided in the previous query.
        :type page_next_record_id: str, optional
        :rtype: HourlyUsageResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["filter_timestamp_start"] = filter_timestamp_start

        if filter_timestamp_end is not unset:
            kwargs["filter_timestamp_end"] = filter_timestamp_end

        kwargs["filter_product_families"] = filter_product_families

        if filter_include_descendants is not unset:
            kwargs["filter_include_descendants"] = filter_include_descendants

        if filter_versions is not unset:
            kwargs["filter_versions"] = filter_versions

        if page_limit is not unset:
            kwargs["page_limit"] = page_limit

        if page_next_record_id is not unset:
            kwargs["page_next_record_id"] = page_next_record_id

        return self._get_hourly_usage_endpoint.call_with_http_info(**kwargs)

    def get_usage_application_security_monitoring(
        self,
        start_hr: datetime,
        *,
        end_hr: Union[datetime, UnsetType] = unset,
    ) -> UsageApplicationSecurityMonitoringResponse:
        """Get hourly usage for application security.

        Get hourly usage for application security .
        **Note:** hourly usage data for all products is now available in the `Get hourly usage by product family API <https://docs.datadoghq.com/api/latest/usage-metering/#get-hourly-usage-by-product-family>`_

        :param start_hr: Datetime in ISO-8601 format, UTC, precise to hour: ``[YYYY-MM-DDThh]`` for usage beginning at this hour.
        :type start_hr: datetime
        :param end_hr: Datetime in ISO-8601 format, UTC, precise to hour: ``[YYYY-MM-DDThh]`` for usage ending
            **before** this hour.
        :type end_hr: datetime, optional
        :rtype: UsageApplicationSecurityMonitoringResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["start_hr"] = start_hr

        if end_hr is not unset:
            kwargs["end_hr"] = end_hr

        return self._get_usage_application_security_monitoring_endpoint.call_with_http_info(**kwargs)

    def get_usage_lambda_traced_invocations(
        self,
        start_hr: datetime,
        *,
        end_hr: Union[datetime, UnsetType] = unset,
    ) -> UsageLambdaTracedInvocationsResponse:
        """Get hourly usage for lambda traced invocations.

        Get hourly usage for lambda traced invocations.
        **Note:** hourly usage data for all products is now available in the `Get hourly usage by product family API <https://docs.datadoghq.com/api/latest/usage-metering/#get-hourly-usage-by-product-family>`_

        :param start_hr: Datetime in ISO-8601 format, UTC, precise to hour: ``[YYYY-MM-DDThh]`` for usage beginning at this hour.
        :type start_hr: datetime
        :param end_hr: Datetime in ISO-8601 format, UTC, precise to hour: ``[YYYY-MM-DDThh]`` for usage ending
            **before** this hour.
        :type end_hr: datetime, optional
        :rtype: UsageLambdaTracedInvocationsResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["start_hr"] = start_hr

        if end_hr is not unset:
            kwargs["end_hr"] = end_hr

        return self._get_usage_lambda_traced_invocations_endpoint.call_with_http_info(**kwargs)

    def get_usage_observability_pipelines(
        self,
        start_hr: datetime,
        *,
        end_hr: Union[datetime, UnsetType] = unset,
    ) -> UsageObservabilityPipelinesResponse:
        """Get hourly usage for observability pipelines.

        Get hourly usage for observability pipelines.
        **Note:** hourly usage data for all products is now available in the `Get hourly usage by product family API <https://docs.datadoghq.com/api/latest/usage-metering/#get-hourly-usage-by-product-family>`_

        :param start_hr: Datetime in ISO-8601 format, UTC, precise to hour: ``[YYYY-MM-DDThh]`` for usage beginning at this hour.
        :type start_hr: datetime
        :param end_hr: Datetime in ISO-8601 format, UTC, precise to hour: ``[YYYY-MM-DDThh]`` for usage ending
            **before** this hour.
        :type end_hr: datetime, optional
        :rtype: UsageObservabilityPipelinesResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["start_hr"] = start_hr

        if end_hr is not unset:
            kwargs["end_hr"] = end_hr

        return self._get_usage_observability_pipelines_endpoint.call_with_http_info(**kwargs)
