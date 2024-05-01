# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Any, Dict

from datadog_api_client.api_client import ApiClient, Endpoint as _Endpoint
from datadog_api_client.configuration import Configuration
from datadog_api_client.v2.model.spans_metrics_response import SpansMetricsResponse
from datadog_api_client.v2.model.spans_metric_response import SpansMetricResponse
from datadog_api_client.v2.model.spans_metric_create_request import SpansMetricCreateRequest
from datadog_api_client.v2.model.spans_metric_update_request import SpansMetricUpdateRequest


class SpansMetricsApi:
    """
    Manage configuration of `span-based metrics <https://app.datadoghq.com/apm/traces/generate-metrics>`_ for your organization.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient(Configuration())
        self.api_client = api_client

        self._create_spans_metric_endpoint = _Endpoint(
            settings={
                "response_type": (SpansMetricResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v2/apm/config/metrics",
                "operation_id": "create_spans_metric",
                "http_method": "POST",
                "version": "v2",
                "servers": None,
            },
            params_map={
                "body": {
                    "required": True,
                    "openapi_types": (SpansMetricCreateRequest,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

        self._delete_spans_metric_endpoint = _Endpoint(
            settings={
                "response_type": None,
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v2/apm/config/metrics/{metric_id}",
                "operation_id": "delete_spans_metric",
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

        self._get_spans_metric_endpoint = _Endpoint(
            settings={
                "response_type": (SpansMetricResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v2/apm/config/metrics/{metric_id}",
                "operation_id": "get_spans_metric",
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

        self._list_spans_metrics_endpoint = _Endpoint(
            settings={
                "response_type": (SpansMetricsResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v2/apm/config/metrics",
                "operation_id": "list_spans_metrics",
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

        self._update_spans_metric_endpoint = _Endpoint(
            settings={
                "response_type": (SpansMetricResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v2/apm/config/metrics/{metric_id}",
                "operation_id": "update_spans_metric",
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
                    "openapi_types": (SpansMetricUpdateRequest,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

    def create_spans_metric(
        self,
        body: SpansMetricCreateRequest,
    ) -> SpansMetricResponse:
        """Create a span-based metric.

        Create a metric based on your ingested spans in your organization.
        Returns the span-based metric object from the request body when the request is successful.

        :param body: The definition of the new span-based metric.
        :type body: SpansMetricCreateRequest
        :rtype: SpansMetricResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["body"] = body

        return self._create_spans_metric_endpoint.call_with_http_info(**kwargs)

    def delete_spans_metric(
        self,
        metric_id: str,
    ) -> None:
        """Delete a span-based metric.

        Delete a specific span-based metric from your organization.

        :param metric_id: The name of the span-based metric.
        :type metric_id: str
        :rtype: None
        """
        kwargs: Dict[str, Any] = {}
        kwargs["metric_id"] = metric_id

        return self._delete_spans_metric_endpoint.call_with_http_info(**kwargs)

    def get_spans_metric(
        self,
        metric_id: str,
    ) -> SpansMetricResponse:
        """Get a span-based metric.

        Get a specific span-based metric from your organization.

        :param metric_id: The name of the span-based metric.
        :type metric_id: str
        :rtype: SpansMetricResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["metric_id"] = metric_id

        return self._get_spans_metric_endpoint.call_with_http_info(**kwargs)

    def list_spans_metrics(
        self,
    ) -> SpansMetricsResponse:
        """Get all span-based metrics.

        Get the list of configured span-based metrics with their definitions.

        :rtype: SpansMetricsResponse
        """
        kwargs: Dict[str, Any] = {}
        return self._list_spans_metrics_endpoint.call_with_http_info(**kwargs)

    def update_spans_metric(
        self,
        metric_id: str,
        body: SpansMetricUpdateRequest,
    ) -> SpansMetricResponse:
        """Update a span-based metric.

        Update a specific span-based metric from your organization.
        Returns the span-based metric object from the request body when the request is successful.

        :param metric_id: The name of the span-based metric.
        :type metric_id: str
        :param body: New definition of the span-based metric.
        :type body: SpansMetricUpdateRequest
        :rtype: SpansMetricResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["metric_id"] = metric_id

        kwargs["body"] = body

        return self._update_spans_metric_endpoint.call_with_http_info(**kwargs)
