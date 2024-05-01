# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Any, Dict, List

from datadog_api_client.api_client import ApiClient, Endpoint as _Endpoint
from datadog_api_client.configuration import Configuration
from datadog_api_client.v1.model.aws_account_and_lambda_request import AWSAccountAndLambdaRequest
from datadog_api_client.v1.model.aws_logs_list_response import AWSLogsListResponse
from datadog_api_client.v1.model.aws_logs_async_response import AWSLogsAsyncResponse
from datadog_api_client.v1.model.aws_logs_list_services_response import AWSLogsListServicesResponse
from datadog_api_client.v1.model.aws_logs_services_request import AWSLogsServicesRequest


class AWSLogsIntegrationApi:
    """
    Configure your Datadog-AWS-Logs integration directly through Datadog API.
    For more information, see the `AWS integration page <https://docs.datadoghq.com/api/?lang=bash#integration-aws-logs>`_.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient(Configuration())
        self.api_client = api_client

        self._check_aws_logs_lambda_async_endpoint = _Endpoint(
            settings={
                "response_type": (AWSLogsAsyncResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v1/integration/aws/logs/check_async",
                "operation_id": "check_aws_logs_lambda_async",
                "http_method": "POST",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "body": {
                    "required": True,
                    "openapi_types": (AWSAccountAndLambdaRequest,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

        self._check_aws_logs_services_async_endpoint = _Endpoint(
            settings={
                "response_type": (AWSLogsAsyncResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v1/integration/aws/logs/services_async",
                "operation_id": "check_aws_logs_services_async",
                "http_method": "POST",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "body": {
                    "required": True,
                    "openapi_types": (AWSLogsServicesRequest,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

        self._create_aws_lambda_arn_endpoint = _Endpoint(
            settings={
                "response_type": (dict,),
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v1/integration/aws/logs",
                "operation_id": "create_aws_lambda_arn",
                "http_method": "POST",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "body": {
                    "required": True,
                    "openapi_types": (AWSAccountAndLambdaRequest,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

        self._delete_aws_lambda_arn_endpoint = _Endpoint(
            settings={
                "response_type": (dict,),
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v1/integration/aws/logs",
                "operation_id": "delete_aws_lambda_arn",
                "http_method": "DELETE",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "body": {
                    "required": True,
                    "openapi_types": (AWSAccountAndLambdaRequest,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

        self._enable_aws_log_services_endpoint = _Endpoint(
            settings={
                "response_type": (dict,),
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v1/integration/aws/logs/services",
                "operation_id": "enable_aws_log_services",
                "http_method": "POST",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "body": {
                    "required": True,
                    "openapi_types": (AWSLogsServicesRequest,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

        self._list_aws_logs_integrations_endpoint = _Endpoint(
            settings={
                "response_type": ([AWSLogsListResponse],),
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v1/integration/aws/logs",
                "operation_id": "list_aws_logs_integrations",
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

        self._list_aws_logs_services_endpoint = _Endpoint(
            settings={
                "response_type": ([AWSLogsListServicesResponse],),
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v1/integration/aws/logs/services",
                "operation_id": "list_aws_logs_services",
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

    def check_aws_logs_lambda_async(
        self,
        body: AWSAccountAndLambdaRequest,
    ) -> AWSLogsAsyncResponse:
        """Check that an AWS Lambda Function exists.

        Test if permissions are present to add a log-forwarding triggers for the given services and AWS account. The input
        is the same as for Enable an AWS service log collection. Subsequent requests will always repeat the above, so this
        endpoint can be polled intermittently instead of blocking.

        * Returns a status of 'created' when it's checking if the Lambda exists in the account.
        * Returns a status of 'waiting' while checking.
        * Returns a status of 'checked and ok' if the Lambda exists.
        * Returns a status of 'error' if the Lambda does not exist.

        :param body: Check AWS Log Lambda Async request body.
        :type body: AWSAccountAndLambdaRequest
        :rtype: AWSLogsAsyncResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["body"] = body

        return self._check_aws_logs_lambda_async_endpoint.call_with_http_info(**kwargs)

    def check_aws_logs_services_async(
        self,
        body: AWSLogsServicesRequest,
    ) -> AWSLogsAsyncResponse:
        """Check permissions for log services.

        Test if permissions are present to add log-forwarding triggers for the
        given services and AWS account. Input is the same as for ``EnableAWSLogServices``.
        Done async, so can be repeatedly polled in a non-blocking fashion until
        the async request completes.

        * Returns a status of ``created`` when it's checking if the permissions exists
          in the AWS account.
        * Returns a status of ``waiting`` while checking.
        * Returns a status of ``checked and ok`` if the Lambda exists.
        * Returns a status of ``error`` if the Lambda does not exist.

        :param body: Check AWS Logs Async Services request body.
        :type body: AWSLogsServicesRequest
        :rtype: AWSLogsAsyncResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["body"] = body

        return self._check_aws_logs_services_async_endpoint.call_with_http_info(**kwargs)

    def create_aws_lambda_arn(
        self,
        body: AWSAccountAndLambdaRequest,
    ) -> dict:
        """Add AWS Log Lambda ARN.

        Attach the Lambda ARN of the Lambda created for the Datadog-AWS log collection to your AWS account ID to enable log collection.

        :param body: AWS Log Lambda Async request body.
        :type body: AWSAccountAndLambdaRequest
        :rtype: dict
        """
        kwargs: Dict[str, Any] = {}
        kwargs["body"] = body

        return self._create_aws_lambda_arn_endpoint.call_with_http_info(**kwargs)

    def delete_aws_lambda_arn(
        self,
        body: AWSAccountAndLambdaRequest,
    ) -> dict:
        """Delete an AWS Logs integration.

        Delete a Datadog-AWS logs configuration by removing the specific Lambda ARN associated with a given AWS account.

        :param body: Delete AWS Lambda ARN request body.
        :type body: AWSAccountAndLambdaRequest
        :rtype: dict
        """
        kwargs: Dict[str, Any] = {}
        kwargs["body"] = body

        return self._delete_aws_lambda_arn_endpoint.call_with_http_info(**kwargs)

    def enable_aws_log_services(
        self,
        body: AWSLogsServicesRequest,
    ) -> dict:
        """Enable an AWS Logs integration.

        Enable automatic log collection for a list of services. This should be run after running ``CreateAWSLambdaARN`` to save the configuration.

        :param body: Enable AWS Log Services request body.
        :type body: AWSLogsServicesRequest
        :rtype: dict
        """
        kwargs: Dict[str, Any] = {}
        kwargs["body"] = body

        return self._enable_aws_log_services_endpoint.call_with_http_info(**kwargs)

    def list_aws_logs_integrations(
        self,
    ) -> List[AWSLogsListResponse]:
        """List all AWS Logs integrations.

        List all Datadog-AWS Logs integrations configured in your Datadog account.

        :rtype: [AWSLogsListResponse]
        """
        kwargs: Dict[str, Any] = {}
        return self._list_aws_logs_integrations_endpoint.call_with_http_info(**kwargs)

    def list_aws_logs_services(
        self,
    ) -> List[AWSLogsListServicesResponse]:
        """Get list of AWS log ready services.

        Get the list of current AWS services that Datadog offers automatic log collection. Use returned service IDs with the services parameter for the Enable an AWS service log collection API endpoint.

        :rtype: [AWSLogsListServicesResponse]
        """
        kwargs: Dict[str, Any] = {}
        return self._list_aws_logs_services_endpoint.call_with_http_info(**kwargs)
