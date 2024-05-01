# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Any, Dict, Union

from datadog_api_client.api_client import ApiClient, Endpoint as _Endpoint
from datadog_api_client.configuration import Configuration
from datadog_api_client.model_utils import (
    file_type,
    UnsetType,
    unset,
)


class OrganizationsApi:
    """
    Create, edit, and manage your organizations. Read more about `multi-org accounts <https://docs.datadoghq.com/account_management/multi_organization>`_.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient(Configuration())
        self.api_client = api_client

        self._upload_idp_metadata_endpoint = _Endpoint(
            settings={
                "response_type": None,
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v2/saml_configurations/idp_metadata",
                "operation_id": "upload_idp_metadata",
                "http_method": "POST",
                "version": "v2",
                "servers": None,
            },
            params_map={
                "idp_file": {
                    "openapi_types": (file_type,),
                    "attribute": "idp_file",
                    "location": "form",
                },
            },
            headers_map={"accept": ["*/*"], "content_type": ["multipart/form-data"]},
            api_client=api_client,
        )

    def upload_idp_metadata(
        self,
        *,
        idp_file: Union[file_type, UnsetType] = unset,
    ) -> None:
        """Upload IdP metadata.

        Endpoint for uploading IdP metadata for SAML setup.

        Use this endpoint to upload or replace IdP metadata for SAML login configuration.

        :param idp_file: The IdP metadata XML file
        :type idp_file: file_type, optional
        :rtype: None
        """
        kwargs: Dict[str, Any] = {}
        if idp_file is not unset:
            kwargs["idp_file"] = idp_file

        return self._upload_idp_metadata_endpoint.call_with_http_info(**kwargs)
