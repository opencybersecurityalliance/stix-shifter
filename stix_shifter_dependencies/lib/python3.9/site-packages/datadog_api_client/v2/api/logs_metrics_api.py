# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Any, Dict

from datadog_api_client.api_client import ApiClient, Endpoint as _Endpoint
from datadog_api_client.configuration import Configuration
from datadog_api_client.v2.model.logs_metrics_response import LogsMetricsResponse
from datadog_api_client.v2.model.logs_metric_response import LogsMetricResponse
from datadog_api_client.v2.model.logs_metric_create_request import LogsMetricCreateRequest
from datadog_api_client.v2.model.logs_metric_update_request import LogsMetricUpdateRequest


class LogsMetricsApi:
    """
    Manage configuration of `log-based metrics <https://app.datadoghq.com/logs/pipelines/generate-metrics>`_ for your organization.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient(Configuration())
        self.api_client = api_client

        self._create_logs_metric_endpoint = _Endpoint(
            settings={
                "response_type": (LogsMetricResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v2/logs/config/metrics",
                "operation_id": "create_logs_metric",
                "http_method": "POST",
                "version": "v2",
                "servers": None,
            },
            params_map={
                "body": {
                    "required": True,
                    "openapi_types": (LogsMetricCreateRequest,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

        self._delete_logs_metric_endpoint = _Endpoint(
            settings={
                "response_type": None,
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v2/logs/config/metrics/{metric_id}",
                "operation_id": "delete_logs_metric",
                "http_method": "DELETE",
                "version": "v2",
                "servers": None,
            },
            params_map={
                "metric_id": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "metric_id",
                    "location": "path",
                },
            },
            headers_map={
                "accept": ["*/*"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._get_logs_metric_endpoint = _Endpoint(
            settings={
                "response_type": (LogsMetricResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v2/logs/config/metrics/{metric_id}",
                "operation_id": "get_logs_metric",
                "http_method": "GET",
                "version": "v2",
                "servers": None,
            },
            params_map={
                "metric_id": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "metric_id",
                    "location": "path",
                },
            },
            headers_map={
                "accept": ["application/json"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._list_logs_metrics_endpoint = _Endpoint(
            settings={
                "response_type": (LogsMetricsResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v2/logs/config/metrics",
                "operation_id": "list_logs_metrics",
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

        self._update_logs_metric_endpoint = _Endpoint(
            settings={
                "response_type": (LogsMetricResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v2/logs/config/metrics/{metric_id}",
                "operation_id": "update_logs_metric",
                "http_method": "PATCH",
                "version": "v2",
                "servers": None,
            },
            params_map={
                "metric_id": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "metric_id",
                    "location": "path",
                },
                "body": {
                    "required": True,
                    "openapi_types": (LogsMetricUpdateRequest,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

    def create_logs_metric(
        self,
        body: LogsMetricCreateRequest,
    ) -> LogsMetricResponse:
        """Create a log-based metric.

        Create a metric based on your ingested logs in your organization.
        Returns the log-based metric object from the request body when the request is successful.

        :param body: The definition of the new log-based metric.
        :type body: LogsMetricCreateRequest
        :rtype: LogsMetricResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["body"] = body

        return self._create_logs_metric_endpoint.call_with_http_info(**kwargs)

    def delete_logs_metric(
        self,
        metric_id: str,
    ) -> None:
        """Delete a log-based metric.

        Delete a specific log-based metric from your organization.

        :param metric_id: The name of the log-based metric.
        :type metric_id: str
        :rtype: None
        """
        kwargs: Dict[str, Any] = {}
        kwargs["metric_id"] = metric_id

        return self._delete_logs_metric_endpoint.call_with_http_info(**kwargs)

    def get_logs_metric(
        self,
        metric_id: str,
    ) -> LogsMetricResponse:
        """Get a log-based metric.

        Get a specific log-based metric from your organization.

        :param metric_id: The name of the log-based metric.
        :type metric_id: str
        :rtype: LogsMetricResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["metric_id"] = metric_id

        return self._get_logs_metric_endpoint.call_with_http_info(**kwargs)

    def list_logs_metrics(
        self,
    ) -> LogsMetricsResponse:
        """Get all log-based metrics.

        Get the list of configured log-based metrics with their definitions.

        :rtype: LogsMetricsResponse
        """
        kwargs: Dict[str, Any] = {}
        return self._list_logs_metrics_endpoint.call_with_http_info(**kwargs)

    def update_logs_metric(
        self,
        metric_id: str,
        body: LogsMetricUpdateRequest,
    ) -> LogsMetricResponse:
        """Update a log-based metric.

        Update a specific log-based metric from your organization.
        Returns the log-based metric object from the request body when the request is successful.

        :param metric_id: The name of the log-based metric.
        :type metric_id: str
        :param body: New definition of the log-based metric.
        :type body: LogsMetricUpdateRequest
        :rtype: LogsMetricResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["metric_id"] = metric_id

        kwargs["body"] = body

        return self._update_logs_metric_endpoint.call_with_http_info(**kwargs)
