# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Any, Dict

from datadog_api_client.api_client import ApiClient, Endpoint as _Endpoint
from datadog_api_client.configuration import Configuration
from datadog_api_client.model_utils import (
    file_type,
)
from datadog_api_client.v1.model.organization_list_response import OrganizationListResponse
from datadog_api_client.v1.model.organization_create_response import OrganizationCreateResponse
from datadog_api_client.v1.model.organization_create_body import OrganizationCreateBody
from datadog_api_client.v1.model.organization_response import OrganizationResponse
from datadog_api_client.v1.model.organization import Organization
from datadog_api_client.v1.model.org_downgraded_response import OrgDowngradedResponse
from datadog_api_client.v1.model.idp_response import IdpResponse


class OrganizationsApi:
    """
    Create, edit, and manage your organizations. Read more about `multi-org accounts <https://docs.datadoghq.com/account_management/multi_organization>`_.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient(Configuration())
        self.api_client = api_client

        self._create_child_org_endpoint = _Endpoint(
            settings={
                "response_type": (OrganizationCreateResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v1/org",
                "operation_id": "create_child_org",
                "http_method": "POST",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "body": {
                    "required": True,
                    "openapi_types": (OrganizationCreateBody,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

        self._downgrade_org_endpoint = _Endpoint(
            settings={
                "response_type": (OrgDowngradedResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v1/org/{public_id}/downgrade",
                "operation_id": "downgrade_org",
                "http_method": "POST",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "public_id": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "public_id",
                    "location": "path",
                },
            },
            headers_map={
                "accept": ["application/json"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._get_org_endpoint = _Endpoint(
            settings={
                "response_type": (OrganizationResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v1/org/{public_id}",
                "operation_id": "get_org",
                "http_method": "GET",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "public_id": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "public_id",
                    "location": "path",
                },
            },
            headers_map={
                "accept": ["application/json"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._list_orgs_endpoint = _Endpoint(
            settings={
                "response_type": (OrganizationListResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v1/org",
                "operation_id": "list_orgs",
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

        self._update_org_endpoint = _Endpoint(
            settings={
                "response_type": (OrganizationResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v1/org/{public_id}",
                "operation_id": "update_org",
                "http_method": "PUT",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "public_id": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "public_id",
                    "location": "path",
                },
                "body": {
                    "required": True,
                    "openapi_types": (Organization,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

        self._upload_idp_for_org_endpoint = _Endpoint(
            settings={
                "response_type": (IdpResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v1/org/{public_id}/idp_metadata",
                "operation_id": "upload_idp_for_org",
                "http_method": "POST",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "public_id": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "public_id",
                    "location": "path",
                },
                "idp_file": {
                    "required": True,
                    "openapi_types": (file_type,),
                    "attribute": "idp_file",
                    "location": "form",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["multipart/form-data"]},
            api_client=api_client,
        )

    def create_child_org(
        self,
        body: OrganizationCreateBody,
    ) -> OrganizationCreateResponse:
        """Create a child organization.

        Create a child organization.

        This endpoint requires the
        `multi-organization account <https://docs.datadoghq.com/account_management/multi_organization/>`_
        feature and must be enabled by
        `contacting support <https://docs.datadoghq.com/help/>`_.

        Once a new child organization is created, you can interact with it
        by using the ``org.public_id`` , ``api_key.key`` , and
        ``application_key.hash`` provided in the response.

        :param body: Organization object that needs to be created
        :type body: OrganizationCreateBody
        :rtype: OrganizationCreateResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["body"] = body

        return self._create_child_org_endpoint.call_with_http_info(**kwargs)

    def downgrade_org(
        self,
        public_id: str,
    ) -> OrgDowngradedResponse:
        """Spin-off Child Organization.

        Only available for MSP customers. Removes a child organization from the hierarchy of the master organization and places the child organization on a 30-day trial.

        :param public_id: The ``public_id`` of the organization you are operating within.
        :type public_id: str
        :rtype: OrgDowngradedResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["public_id"] = public_id

        return self._downgrade_org_endpoint.call_with_http_info(**kwargs)

    def get_org(
        self,
        public_id: str,
    ) -> OrganizationResponse:
        """Get organization information.

        Get organization information.

        :param public_id: The ``public_id`` of the organization you are operating within.
        :type public_id: str
        :rtype: OrganizationResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["public_id"] = public_id

        return self._get_org_endpoint.call_with_http_info(**kwargs)

    def list_orgs(
        self,
    ) -> OrganizationListResponse:
        """List your managed organizations.

        This endpoint returns data on your top-level organization.

        :rtype: OrganizationListResponse
        """
        kwargs: Dict[str, Any] = {}
        return self._list_orgs_endpoint.call_with_http_info(**kwargs)

    def update_org(
        self,
        public_id: str,
        body: Organization,
    ) -> OrganizationResponse:
        """Update your organization.

        Update your organization.

        :param public_id: The ``public_id`` of the organization you are operating within.
        :type public_id: str
        :type body: Organization
        :rtype: OrganizationResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["public_id"] = public_id

        kwargs["body"] = body

        return self._update_org_endpoint.call_with_http_info(**kwargs)

    def upload_idp_for_org(
        self,
        public_id: str,
        idp_file: file_type,
    ) -> IdpResponse:
        """Upload IdP metadata.

        There are a couple of options for updating the Identity Provider (IdP)
        metadata from your SAML IdP.

        *
          **Multipart Form-Data** : Post the IdP metadata file using a form post.

        *
          **XML Body:** Post the IdP metadata file as the body of the request.

        :param public_id: The ``public_id`` of the organization you are operating with
        :type public_id: str
        :param idp_file: The path to the XML metadata file you wish to upload.
        :type idp_file: file_type
        :rtype: IdpResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["public_id"] = public_id

        kwargs["idp_file"] = idp_file

        return self._upload_idp_for_org_endpoint.call_with_http_info(**kwargs)
