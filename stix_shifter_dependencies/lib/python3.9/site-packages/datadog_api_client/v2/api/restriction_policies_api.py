# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Any, Dict

from datadog_api_client.api_client import ApiClient, Endpoint as _Endpoint
from datadog_api_client.configuration import Configuration
from datadog_api_client.v2.model.restriction_policy_response import RestrictionPolicyResponse
from datadog_api_client.v2.model.restriction_policy_update_request import RestrictionPolicyUpdateRequest


class RestrictionPoliciesApi:
    """
    A restriction policy defines the access control rules for a resource, mapping a set of relations
    (such as editor and viewer) to a set of allowed principals (such as roles). The restriction policy
    determines who is authorized to perform what actions on the resource.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient(Configuration())
        self.api_client = api_client

        self._delete_restriction_policy_endpoint = _Endpoint(
            settings={
                "response_type": None,
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v2/restriction_policy/{resource_id}",
                "operation_id": "delete_restriction_policy",
                "http_method": "DELETE",
                "version": "v2",
                "servers": None,
            },
            params_map={
                "resource_id": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "resource_id",
                    "location": "path",
                },
            },
            headers_map={
                "accept": ["*/*"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._get_restriction_policy_endpoint = _Endpoint(
            settings={
                "response_type": (RestrictionPolicyResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v2/restriction_policy/{resource_id}",
                "operation_id": "get_restriction_policy",
                "http_method": "GET",
                "version": "v2",
                "servers": None,
            },
            params_map={
                "resource_id": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "resource_id",
                    "location": "path",
                },
            },
            headers_map={
                "accept": ["application/json"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._update_restriction_policy_endpoint = _Endpoint(
            settings={
                "response_type": (RestrictionPolicyResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v2/restriction_policy/{resource_id}",
                "operation_id": "update_restriction_policy",
                "http_method": "POST",
                "version": "v2",
                "servers": None,
            },
            params_map={
                "resource_id": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "resource_id",
                    "location": "path",
                },
                "body": {
                    "required": True,
                    "openapi_types": (RestrictionPolicyUpdateRequest,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

    def delete_restriction_policy(
        self,
        resource_id: str,
    ) -> None:
        """Delete a restriction policy.

        Deletes the restriction policy associated with a specified resource.

        :param resource_id: Identifier, formatted as ``type:id``. Supported types: ``connection`` , ``dashboard`` , ``notebook`` , ``security-rule`` , ``slo``.
        :type resource_id: str
        :rtype: None
        """
        kwargs: Dict[str, Any] = {}
        kwargs["resource_id"] = resource_id

        return self._delete_restriction_policy_endpoint.call_with_http_info(**kwargs)

    def get_restriction_policy(
        self,
        resource_id: str,
    ) -> RestrictionPolicyResponse:
        """Get a restriction policy.

        Retrieves the restriction policy associated with a specified resource.

        :param resource_id: Identifier, formatted as ``type:id``. Supported types: ``connection`` , ``dashboard`` , ``notebook`` , ``security-rule`` , ``slo``.
        :type resource_id: str
        :rtype: RestrictionPolicyResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["resource_id"] = resource_id

        return self._get_restriction_policy_endpoint.call_with_http_info(**kwargs)

    def update_restriction_policy(
        self,
        resource_id: str,
        body: RestrictionPolicyUpdateRequest,
    ) -> RestrictionPolicyResponse:
        """Update a restriction policy.

        Updates the restriction policy associated with a resource.

        **Supported resources**

        Restriction policies can be applied to the following resources:

        * Connections: ``connection``
        * Dashboards: ``dashboard``
        * Notebooks: ``notebook``
        * Security Rules: ``security-rule``
        * Service Level Objectives: ``slo``

        **Supported relations for resources**

        .. list-table::
           :header-rows: 1

           * - Resource Type
             - Supported Relations
           * - Connections
             - ``viewer`` , ``editor`` , ``resolver``
           * - Dashboards
             - ``viewer`` , ``editor``
           * - Notebooks
             - ``viewer`` , ``editor``
           * - Security Rules
             - ``viewer`` , ``editor``
           * - Service Level Objectives
             - ``viewer`` , ``editor``


        :param resource_id: Identifier, formatted as ``type:id``. Supported types: ``connection`` , ``dashboard`` , ``notebook`` , ``security-rule`` , ``slo``.
        :type resource_id: str
        :param body: Restriction policy payload
        :type body: RestrictionPolicyUpdateRequest
        :rtype: RestrictionPolicyResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["resource_id"] = resource_id

        kwargs["body"] = body

        return self._update_restriction_policy_endpoint.call_with_http_info(**kwargs)
