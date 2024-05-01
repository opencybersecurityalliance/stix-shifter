# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Any, Dict

from datadog_api_client.api_client import ApiClient, Endpoint as _Endpoint
from datadog_api_client.configuration import Configuration
from datadog_api_client.v1.model.successful_signal_update_response import SuccessfulSignalUpdateResponse
from datadog_api_client.v1.model.add_signal_to_incident_request import AddSignalToIncidentRequest
from datadog_api_client.v1.model.signal_assignee_update_request import SignalAssigneeUpdateRequest
from datadog_api_client.v1.model.signal_state_update_request import SignalStateUpdateRequest


class SecurityMonitoringApi:
    """
    Detection rules for generating signals and listing of generated
    signals.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient(Configuration())
        self.api_client = api_client

        self._add_security_monitoring_signal_to_incident_endpoint = _Endpoint(
            settings={
                "response_type": (SuccessfulSignalUpdateResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v1/security_analytics/signals/{signal_id}/add_to_incident",
                "operation_id": "add_security_monitoring_signal_to_incident",
                "http_method": "PATCH",
                "version": "v1",
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
                    "openapi_types": (AddSignalToIncidentRequest,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

        self._edit_security_monitoring_signal_assignee_endpoint = _Endpoint(
            settings={
                "response_type": (SuccessfulSignalUpdateResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v1/security_analytics/signals/{signal_id}/assignee",
                "operation_id": "edit_security_monitoring_signal_assignee",
                "http_method": "PATCH",
                "version": "v1",
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
                    "openapi_types": (SignalAssigneeUpdateRequest,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

        self._edit_security_monitoring_signal_state_endpoint = _Endpoint(
            settings={
                "response_type": (SuccessfulSignalUpdateResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v1/security_analytics/signals/{signal_id}/state",
                "operation_id": "edit_security_monitoring_signal_state",
                "http_method": "PATCH",
                "version": "v1",
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
                    "openapi_types": (SignalStateUpdateRequest,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

    def add_security_monitoring_signal_to_incident(
        self,
        signal_id: str,
        body: AddSignalToIncidentRequest,
    ) -> SuccessfulSignalUpdateResponse:
        """Add a security signal to an incident.

        Add a security signal to an incident. This makes it possible to search for signals by incident within the signal explorer and to view the signals on the incident timeline.

        :param signal_id: The ID of the signal.
        :type signal_id: str
        :param body: Attributes describing the signal update.
        :type body: AddSignalToIncidentRequest
        :rtype: SuccessfulSignalUpdateResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["signal_id"] = signal_id

        kwargs["body"] = body

        return self._add_security_monitoring_signal_to_incident_endpoint.call_with_http_info(**kwargs)

    def edit_security_monitoring_signal_assignee(
        self,
        signal_id: str,
        body: SignalAssigneeUpdateRequest,
    ) -> SuccessfulSignalUpdateResponse:
        """Modify the triage assignee of a security signal.

        Modify the triage assignee of a security signal.

        :param signal_id: The ID of the signal.
        :type signal_id: str
        :param body: Attributes describing the signal update.
        :type body: SignalAssigneeUpdateRequest
        :rtype: SuccessfulSignalUpdateResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["signal_id"] = signal_id

        kwargs["body"] = body

        return self._edit_security_monitoring_signal_assignee_endpoint.call_with_http_info(**kwargs)

    def edit_security_monitoring_signal_state(
        self,
        signal_id: str,
        body: SignalStateUpdateRequest,
    ) -> SuccessfulSignalUpdateResponse:
        """Change the triage state of a security signal.

        Change the triage state of a security signal.

        :param signal_id: The ID of the signal.
        :type signal_id: str
        :param body: Attributes describing the signal update.
        :type body: SignalStateUpdateRequest
        :rtype: SuccessfulSignalUpdateResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["signal_id"] = signal_id

        kwargs["body"] = body

        return self._edit_security_monitoring_signal_state_endpoint.call_with_http_info(**kwargs)
