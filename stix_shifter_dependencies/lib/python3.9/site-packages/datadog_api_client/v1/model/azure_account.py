# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import List, Union

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    unset,
    UnsetType,
)


class AzureAccount(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "automute": (bool,),
            "client_id": (str,),
            "client_secret": (str,),
            "errors": ([str],),
            "host_filters": (str,),
            "new_client_id": (str,),
            "new_tenant_name": (str,),
            "tenant_name": (str,),
        }

    attribute_map = {
        "automute": "automute",
        "client_id": "client_id",
        "client_secret": "client_secret",
        "errors": "errors",
        "host_filters": "host_filters",
        "new_client_id": "new_client_id",
        "new_tenant_name": "new_tenant_name",
        "tenant_name": "tenant_name",
    }

    def __init__(
        self_,
        automute: Union[bool, UnsetType] = unset,
        client_id: Union[str, UnsetType] = unset,
        client_secret: Union[str, UnsetType] = unset,
        errors: Union[List[str], UnsetType] = unset,
        host_filters: Union[str, UnsetType] = unset,
        new_client_id: Union[str, UnsetType] = unset,
        new_tenant_name: Union[str, UnsetType] = unset,
        tenant_name: Union[str, UnsetType] = unset,
        **kwargs,
    ):
        """
        Datadog-Azure integrations configured for your organization.

        :param automute: Silence monitors for expected Azure VM shutdowns.
        :type automute: bool, optional

        :param client_id: Your Azure web application ID.
        :type client_id: str, optional

        :param client_secret: Your Azure web application secret key.
        :type client_secret: str, optional

        :param errors: Errors in your configuration.
        :type errors: [str], optional

        :param host_filters: Limit the Azure instances that are pulled into Datadog by using tags.
            Only hosts that match one of the defined tags are imported into Datadog.
        :type host_filters: str, optional

        :param new_client_id: Your New Azure web application ID.
        :type new_client_id: str, optional

        :param new_tenant_name: Your New Azure Active Directory ID.
        :type new_tenant_name: str, optional

        :param tenant_name: Your Azure Active Directory ID.
        :type tenant_name: str, optional
        """
        if automute is not unset:
            kwargs["automute"] = automute
        if client_id is not unset:
            kwargs["client_id"] = client_id
        if client_secret is not unset:
            kwargs["client_secret"] = client_secret
        if errors is not unset:
            kwargs["errors"] = errors
        if host_filters is not unset:
            kwargs["host_filters"] = host_filters
        if new_client_id is not unset:
            kwargs["new_client_id"] = new_client_id
        if new_tenant_name is not unset:
            kwargs["new_tenant_name"] = new_tenant_name
        if tenant_name is not unset:
            kwargs["tenant_name"] = tenant_name
        super().__init__(kwargs)
