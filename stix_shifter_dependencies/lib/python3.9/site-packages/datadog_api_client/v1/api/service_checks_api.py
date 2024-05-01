# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Any, Dict

from datadog_api_client.api_client import ApiClient, Endpoint as _Endpoint
from datadog_api_client.configuration import Configuration
from datadog_api_client.v1.model.intake_payload_accepted import IntakePayloadAccepted
from datadog_api_client.v1.model.service_checks import ServiceChecks


class ServiceChecksApi:
    """
    The service check endpoint allows you to post check statuses for use with monitors.
    Service check messages are limited to 500 characters. If a check is posted with a message
    containing more than 500 characters, only the first 500 characters are displayed. Messages
    are limited for checks with a Critical or Warning status, they are dropped for checks with
    an OK status.

    * `Read more about Service Check monitors. <https://docs.datadoghq.com/monitors/create/types/host/?tab=checkalert>`_
    * `Read more about Process Check monitors. <https://docs.datadoghq.com/monitors/create/types/process_check/?tab=checkalert>`_
    * `Read more about Network Check monitors. <https://docs.datadoghq.com/monitors/create/types/network/?tab=checkalert>`_
    * `Read more about Custom Check monitors. <https://docs.datadoghq.com/monitors/create/types/custom_check/?tab=checkalert>`_
    * `Read more about Service Check and status codes. <https://docs.datadoghq.com/developers/service_checks/>`_
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient(Configuration())
        self.api_client = api_client

        self._submit_service_check_endpoint = _Endpoint(
            settings={
                "response_type": (IntakePayloadAccepted,),
                "auth": ["apiKeyAuth"],
                "endpoint_path": "/api/v1/check_run",
                "operation_id": "submit_service_check",
                "http_method": "POST",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "body": {
                    "required": True,
                    "openapi_types": (ServiceChecks,),
                    "location": "body",
                    "collection_format": "multi",
                },
            },
            headers_map={"accept": ["text/json", "application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

    def submit_service_check(
        self,
        body: ServiceChecks,
    ) -> IntakePayloadAccepted:
        """Submit a Service Check.

        Submit a list of Service Checks.

        **Notes** :

        * A valid API key is required.
        * Service checks can be submitted up to 10 minutes in the past.

        :param body: Service Check request body.
        :type body: ServiceChecks
        :rtype: IntakePayloadAccepted
        """
        kwargs: Dict[str, Any] = {}
        kwargs["body"] = body

        return self._submit_service_check_endpoint.call_with_http_info(**kwargs)
