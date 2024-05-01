# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Any, Dict, Union

from datadog_api_client.api_client import ApiClient, Endpoint as _Endpoint
from datadog_api_client.configuration import Configuration
from datadog_api_client.model_utils import (
    UnsetType,
    unset,
)
from datadog_api_client.v1.model.intake_payload_accepted import IntakePayloadAccepted
from datadog_api_client.v1.model.distribution_points_content_encoding import DistributionPointsContentEncoding
from datadog_api_client.v1.model.distribution_points_payload import DistributionPointsPayload
from datadog_api_client.v1.model.metrics_list_response import MetricsListResponse
from datadog_api_client.v1.model.metric_metadata import MetricMetadata
from datadog_api_client.v1.model.metrics_query_response import MetricsQueryResponse
from datadog_api_client.v1.model.metric_search_response import MetricSearchResponse
from datadog_api_client.v1.model.metric_content_encoding import MetricContentEncoding
from datadog_api_client.v1.model.metrics_payload import MetricsPayload


class MetricsApi:
    """
    The metrics endpoint allows you to:

    * Post metrics data so it can be graphed on Datadog’s dashboards
    * Query metrics from any time period
    * Modify tag configurations for metrics
    * View tags and volumes for metrics

    **Note** : A graph can only contain a set number of points
    and as the timeframe over which a metric is viewed increases,
    aggregation between points occurs to stay below that set number.

    The Post, Patch, and Delete ``manage_tags`` API methods can only be performed by
    a user who has the ``Manage Tags for Metrics`` permission.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient(Configuration())
        self.api_client = api_client

        self._get_metric_metadata_endpoint = _Endpoint(
            settings={
                "response_type": (MetricMetadata,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v1/metrics/{metric_name}",
                "operation_id": "get_metric_metadata",
                "http_method": "GET",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "metric_name": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "metric_name",
                    "location": "path",
                },
            },
            headers_map={
                "accept": ["application/json"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._list_active_metrics_endpoint = _Endpoint(
            settings={
                "response_type": (MetricsListResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v1/metrics",
                "operation_id": "list_active_metrics",
                "http_method": "GET",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "_from": {
                    "required": True,
                    "openapi_types": (int,),
                    "attribute": "from",
                    "location": "query",
                },
                "host": {
                    "openapi_types": (str,),
                    "attribute": "host",
                    "location": "query",
                },
                "tag_filter": {
                    "openapi_types": (str,),
                    "attribute": "tag_filter",
                    "location": "query",
                },
            },
            headers_map={
                "accept": ["application/json"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._list_metrics_endpoint = _Endpoint(
            settings={
                "response_type": (MetricSearchResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v1/search",
                "operation_id": "list_metrics",
                "http_method": "GET",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "q": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "q",
                    "location": "query",
                },
            },
            headers_map={
                "accept": ["application/json"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._query_metrics_endpoint = _Endpoint(
            settings={
                "response_type": (MetricsQueryResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v1/query",
                "operation_id": "query_metrics",
                "http_method": "GET",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "_from": {
                    "required": True,
                    "openapi_types": (int,),
                    "attribute": "from",
                    "location": "query",
                },
                "to": {
                    "required": True,
                    "openapi_types": (int,),
                    "attribute": "to",
                    "location": "query",
                },
                "query": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "query",
                    "location": "query",
                },
            },
            headers_map={
                "accept": ["application/json"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._submit_distribution_points_endpoint = _Endpoint(
            settings={
                "response_type": (IntakePayloadAccepted,),
                "auth": ["apiKeyAuth"],
                "endpoint_path": "/api/v1/distribution_points",
                "operation_id": "submit_distribution_points",
                "http_method": "POST",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "content_encoding": {
                    "openapi_types": (DistributionPointsContentEncoding,),
                    "attribute": "Content-Encoding",
                    "location": "header",
                },
                "body": {
                    "required": True,
                    "openapi_types": (DistributionPointsPayload,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["text/json", "application/json"], "content_type": ["text/json"]},
            api_client=api_client,
        )

        self._submit_metrics_endpoint = _Endpoint(
            settings={
                "response_type": (IntakePayloadAccepted,),
                "auth": ["apiKeyAuth"],
                "endpoint_path": "/api/v1/series",
                "operation_id": "submit_metrics",
                "http_method": "POST",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "content_encoding": {
                    "openapi_types": (MetricContentEncoding,),
                    "attribute": "Content-Encoding",
                    "location": "header",
                },
                "body": {
                    "required": True,
                    "openapi_types": (MetricsPayload,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["text/json", "application/json"], "content_type": ["text/json"]},
            api_client=api_client,
        )

        self._update_metric_metadata_endpoint = _Endpoint(
            settings={
                "response_type": (MetricMetadata,),
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v1/metrics/{metric_name}",
                "operation_id": "update_metric_metadata",
                "http_method": "PUT",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "metric_name": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "metric_name",
                    "location": "path",
                },
                "body": {
                    "required": True,
                    "openapi_types": (MetricMetadata,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

    def get_metric_metadata(
        self,
        metric_name: str,
    ) -> MetricMetadata:
        """Get metric metadata.

        Get metadata about a specific metric.

        :param metric_name: Name of the metric for which to get metadata.
        :type metric_name: str
        :rtype: MetricMetadata
        """
        kwargs: Dict[str, Any] = {}
        kwargs["metric_name"] = metric_name

        return self._get_metric_metadata_endpoint.call_with_http_info(**kwargs)

    def list_active_metrics(
        self,
        _from: int,
        *,
        host: Union[str, UnsetType] = unset,
        tag_filter: Union[str, UnsetType] = unset,
    ) -> MetricsListResponse:
        """Get active metrics list.

        Get the list of actively reporting metrics from a given time until now.

        :param _from: Seconds since the Unix epoch.
        :type _from: int
        :param host: Hostname for filtering the list of metrics returned.
            If set, metrics retrieved are those with the corresponding hostname tag.
        :type host: str, optional
        :param tag_filter: Filter metrics that have been submitted with the given tags. Supports boolean and wildcard expressions.
            Cannot be combined with other filters.
        :type tag_filter: str, optional
        :rtype: MetricsListResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["_from"] = _from

        if host is not unset:
            kwargs["host"] = host

        if tag_filter is not unset:
            kwargs["tag_filter"] = tag_filter

        return self._list_active_metrics_endpoint.call_with_http_info(**kwargs)

    def list_metrics(
        self,
        q: str,
    ) -> MetricSearchResponse:
        """Search metrics.

        Search for metrics from the last 24 hours in Datadog.

        :param q: Query string to search metrics upon. Can optionally be prefixed with ``metrics:``.
        :type q: str
        :rtype: MetricSearchResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["q"] = q

        return self._list_metrics_endpoint.call_with_http_info(**kwargs)

    def query_metrics(
        self,
        _from: int,
        to: int,
        query: str,
    ) -> MetricsQueryResponse:
        """Query timeseries points.

        Query timeseries points.

        :param _from: Start of the queried time period, seconds since the Unix epoch.
        :type _from: int
        :param to: End of the queried time period, seconds since the Unix epoch.
        :type to: int
        :param query: Query string.
        :type query: str
        :rtype: MetricsQueryResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["_from"] = _from

        kwargs["to"] = to

        kwargs["query"] = query

        return self._query_metrics_endpoint.call_with_http_info(**kwargs)

    def submit_distribution_points(
        self,
        body: DistributionPointsPayload,
        *,
        content_encoding: Union[DistributionPointsContentEncoding, UnsetType] = unset,
    ) -> IntakePayloadAccepted:
        """Submit distribution points.

        The distribution points end-point allows you to post distribution data that can be graphed on Datadog’s dashboards.

        :type body: DistributionPointsPayload
        :param content_encoding: HTTP header used to compress the media-type.
        :type content_encoding: DistributionPointsContentEncoding, optional
        :rtype: IntakePayloadAccepted
        """
        kwargs: Dict[str, Any] = {}
        if content_encoding is not unset:
            kwargs["content_encoding"] = content_encoding

        kwargs["body"] = body

        return self._submit_distribution_points_endpoint.call_with_http_info(**kwargs)

    def submit_metrics(
        self,
        body: MetricsPayload,
        *,
        content_encoding: Union[MetricContentEncoding, UnsetType] = unset,
    ) -> IntakePayloadAccepted:
        """Submit metrics.

        The metrics end-point allows you to post time-series data that can be graphed on Datadog’s dashboards.
        The maximum payload size is 3.2 megabytes (3200000 bytes). Compressed payloads must have a decompressed size of less than 62 megabytes (62914560 bytes).

        If you’re submitting metrics directly to the Datadog API without using DogStatsD, expect:

        * 64 bits for the timestamp
        * 64 bits for the value
        * 40 bytes for the metric names
        * 50 bytes for the timeseries
        * The full payload is approximately 100 bytes. However, with the DogStatsD API,
          compression is applied, which reduces the payload size.

        :type body: MetricsPayload
        :param content_encoding: HTTP header used to compress the media-type.
        :type content_encoding: MetricContentEncoding, optional
        :rtype: IntakePayloadAccepted
        """
        kwargs: Dict[str, Any] = {}
        if content_encoding is not unset:
            kwargs["content_encoding"] = content_encoding

        kwargs["body"] = body

        return self._submit_metrics_endpoint.call_with_http_info(**kwargs)

    def update_metric_metadata(
        self,
        metric_name: str,
        body: MetricMetadata,
    ) -> MetricMetadata:
        """Edit metric metadata.

        Edit metadata of a specific metric. Find out more about `supported types <https://docs.datadoghq.com/developers/metrics>`_.

        :param metric_name: Name of the metric for which to edit metadata.
        :type metric_name: str
        :param body: New metadata.
        :type body: MetricMetadata
        :rtype: MetricMetadata
        """
        kwargs: Dict[str, Any] = {}
        kwargs["metric_name"] = metric_name

        kwargs["body"] = body

        return self._update_metric_metadata_endpoint.call_with_http_info(**kwargs)
