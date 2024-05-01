# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Any, Dict

from datadog_api_client.api_client import ApiClient, Endpoint as _Endpoint
from datadog_api_client.configuration import Configuration
from datadog_api_client.v1.model.logs_pipelines_order import LogsPipelinesOrder
from datadog_api_client.v1.model.logs_pipeline_list import LogsPipelineList
from datadog_api_client.v1.model.logs_pipeline import LogsPipeline


class LogsPipelinesApi:
    """
    Pipelines and processors operate on incoming logs, parsing
    and transforming them into structured attributes for easier querying.

    *
      See the `pipelines configuration page <https://app.datadoghq.com/logs/pipelines>`_
      for a list of the pipelines and processors currently configured in web UI.

    *
      Additional API-related information about processors can be found in the
      `processors documentation <https://docs.datadoghq.com/logs/log_configuration/processors/?tab=api#lookup-processor>`_.

    *
      For more information about Pipelines, see the
      `pipeline documentation <https://docs.datadoghq.com/logs/log_configuration/pipelines>`_.

    **Notes:**

    These endpoints are only available for admin users.
    Make sure to use an application key created by an admin.

    **Grok parsing rules may effect JSON output and require
    returned data to be configured before using in a request.**
    For example, if you are using the data returned from a
    request for another request body, and have a parsing rule
    that uses a regex pattern like ``\s`` for spaces, you will
    need to configure all escaped spaces as ``%{space}`` to use
    in the body data.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient(Configuration())
        self.api_client = api_client

        self._create_logs_pipeline_endpoint = _Endpoint(
            settings={
                "response_type": (LogsPipeline,),
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v1/logs/config/pipelines",
                "operation_id": "create_logs_pipeline",
                "http_method": "POST",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "body": {
                    "required": True,
                    "openapi_types": (LogsPipeline,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

        self._delete_logs_pipeline_endpoint = _Endpoint(
            settings={
                "response_type": None,
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v1/logs/config/pipelines/{pipeline_id}",
                "operation_id": "delete_logs_pipeline",
                "http_method": "DELETE",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "pipeline_id": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "pipeline_id",
                    "location": "path",
                },
            },
            headers_map={
                "accept": ["*/*"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._get_logs_pipeline_endpoint = _Endpoint(
            settings={
                "response_type": (LogsPipeline,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v1/logs/config/pipelines/{pipeline_id}",
                "operation_id": "get_logs_pipeline",
                "http_method": "GET",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "pipeline_id": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "pipeline_id",
                    "location": "path",
                },
            },
            headers_map={
                "accept": ["application/json"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._get_logs_pipeline_order_endpoint = _Endpoint(
            settings={
                "response_type": (LogsPipelinesOrder,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v1/logs/config/pipeline-order",
                "operation_id": "get_logs_pipeline_order",
                "http_method": "GET",
                "version": "v1",
                "servers": None,
            },
            params_map={},
            headers_map={
                "accept": ["application/json"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._list_logs_pipelines_endpoint = _Endpoint(
            settings={
                "response_type": (LogsPipelineList,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v1/logs/config/pipelines",
                "operation_id": "list_logs_pipelines",
                "http_method": "GET",
                "version": "v1",
                "servers": None,
            },
            params_map={},
            headers_map={
                "accept": ["application/json"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._update_logs_pipeline_endpoint = _Endpoint(
            settings={
                "response_type": (LogsPipeline,),
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v1/logs/config/pipelines/{pipeline_id}",
                "operation_id": "update_logs_pipeline",
                "http_method": "PUT",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "pipeline_id": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "pipeline_id",
                    "location": "path",
                },
                "body": {
                    "required": True,
                    "openapi_types": (LogsPipeline,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

        self._update_logs_pipeline_order_endpoint = _Endpoint(
            settings={
                "response_type": (LogsPipelinesOrder,),
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v1/logs/config/pipeline-order",
                "operation_id": "update_logs_pipeline_order",
                "http_method": "PUT",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "body": {
                    "required": True,
                    "openapi_types": (LogsPipelinesOrder,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

    def create_logs_pipeline(
        self,
        body: LogsPipeline,
    ) -> LogsPipeline:
        """Create a pipeline.

        Create a pipeline in your organization.

        :param body: Definition of the new pipeline.
        :type body: LogsPipeline
        :rtype: LogsPipeline
        """
        kwargs: Dict[str, Any] = {}
        kwargs["body"] = body

        return self._create_logs_pipeline_endpoint.call_with_http_info(**kwargs)

    def delete_logs_pipeline(
        self,
        pipeline_id: str,
    ) -> None:
        """Delete a pipeline.

        Delete a given pipeline from your organization.
        This endpoint takes no JSON arguments.

        :param pipeline_id: ID of the pipeline to delete.
        :type pipeline_id: str
        :rtype: None
        """
        kwargs: Dict[str, Any] = {}
        kwargs["pipeline_id"] = pipeline_id

        return self._delete_logs_pipeline_endpoint.call_with_http_info(**kwargs)

    def get_logs_pipeline(
        self,
        pipeline_id: str,
    ) -> LogsPipeline:
        """Get a pipeline.

        Get a specific pipeline from your organization.
        This endpoint takes no JSON arguments.

        :param pipeline_id: ID of the pipeline to get.
        :type pipeline_id: str
        :rtype: LogsPipeline
        """
        kwargs: Dict[str, Any] = {}
        kwargs["pipeline_id"] = pipeline_id

        return self._get_logs_pipeline_endpoint.call_with_http_info(**kwargs)

    def get_logs_pipeline_order(
        self,
    ) -> LogsPipelinesOrder:
        """Get pipeline order.

        Get the current order of your pipelines.
        This endpoint takes no JSON arguments.

        :rtype: LogsPipelinesOrder
        """
        kwargs: Dict[str, Any] = {}
        return self._get_logs_pipeline_order_endpoint.call_with_http_info(**kwargs)

    def list_logs_pipelines(
        self,
    ) -> LogsPipelineList:
        """Get all pipelines.

        Get all pipelines from your organization.
        This endpoint takes no JSON arguments.

        :rtype: LogsPipelineList
        """
        kwargs: Dict[str, Any] = {}
        return self._list_logs_pipelines_endpoint.call_with_http_info(**kwargs)

    def update_logs_pipeline(
        self,
        pipeline_id: str,
        body: LogsPipeline,
    ) -> LogsPipeline:
        """Update a pipeline.

        Update a given pipeline configuration to change it’s processors or their order.

        **Note** : Using this method updates your pipeline configuration by **replacing**
        your current configuration with the new one sent to your Datadog organization.

        :param pipeline_id: ID of the pipeline to delete.
        :type pipeline_id: str
        :param body: New definition of the pipeline.
        :type body: LogsPipeline
        :rtype: LogsPipeline
        """
        kwargs: Dict[str, Any] = {}
        kwargs["pipeline_id"] = pipeline_id

        kwargs["body"] = body

        return self._update_logs_pipeline_endpoint.call_with_http_info(**kwargs)

    def update_logs_pipeline_order(
        self,
        body: LogsPipelinesOrder,
    ) -> LogsPipelinesOrder:
        """Update pipeline order.

        Update the order of your pipelines. Since logs are processed sequentially, reordering a pipeline may change
        the structure and content of the data processed by other pipelines and their processors.

        **Note** : Using the ``PUT`` method updates your pipeline order by replacing your current order
        with the new one sent to your Datadog organization.

        :param body: Object containing the new ordered list of pipeline IDs.
        :type body: LogsPipelinesOrder
        :rtype: LogsPipelinesOrder
        """
        kwargs: Dict[str, Any] = {}
        kwargs["body"] = body

        return self._update_logs_pipeline_order_endpoint.call_with_http_info(**kwargs)
