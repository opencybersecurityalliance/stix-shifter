# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Union, TYPE_CHECKING

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    unset,
    UnsetType,
)


if TYPE_CHECKING:
    from datadog_api_client.v1.model.organization_settings_saml import OrganizationSettingsSaml
    from datadog_api_client.v1.model.access_role import AccessRole
    from datadog_api_client.v1.model.organization_settings_saml_autocreate_users_domains import (
        OrganizationSettingsSamlAutocreateUsersDomains,
    )
    from datadog_api_client.v1.model.organization_settings_saml_idp_initiated_login import (
        OrganizationSettingsSamlIdpInitiatedLogin,
    )
    from datadog_api_client.v1.model.organization_settings_saml_strict_mode import OrganizationSettingsSamlStrictMode


class OrganizationSettings(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.organization_settings_saml import OrganizationSettingsSaml
        from datadog_api_client.v1.model.access_role import AccessRole
        from datadog_api_client.v1.model.organization_settings_saml_autocreate_users_domains import (
            OrganizationSettingsSamlAutocreateUsersDomains,
        )
        from datadog_api_client.v1.model.organization_settings_saml_idp_initiated_login import (
            OrganizationSettingsSamlIdpInitiatedLogin,
        )
        from datadog_api_client.v1.model.organization_settings_saml_strict_mode import (
            OrganizationSettingsSamlStrictMode,
        )

        return {
            "private_widget_share": (bool,),
            "saml": (OrganizationSettingsSaml,),
            "saml_autocreate_access_role": (AccessRole,),
            "saml_autocreate_users_domains": (OrganizationSettingsSamlAutocreateUsersDomains,),
            "saml_can_be_enabled": (bool,),
            "saml_idp_endpoint": (str,),
            "saml_idp_initiated_login": (OrganizationSettingsSamlIdpInitiatedLogin,),
            "saml_idp_metadata_uploaded": (bool,),
            "saml_login_url": (str,),
            "saml_strict_mode": (OrganizationSettingsSamlStrictMode,),
        }

    attribute_map = {
        "private_widget_share": "private_widget_share",
        "saml": "saml",
        "saml_autocreate_access_role": "saml_autocreate_access_role",
        "saml_autocreate_users_domains": "saml_autocreate_users_domains",
        "saml_can_be_enabled": "saml_can_be_enabled",
        "saml_idp_endpoint": "saml_idp_endpoint",
        "saml_idp_initiated_login": "saml_idp_initiated_login",
        "saml_idp_metadata_uploaded": "saml_idp_metadata_uploaded",
        "saml_login_url": "saml_login_url",
        "saml_strict_mode": "saml_strict_mode",
    }

    def __init__(
        self_,
        private_widget_share: Union[bool, UnsetType] = unset,
        saml: Union[OrganizationSettingsSaml, UnsetType] = unset,
        saml_autocreate_access_role: Union[AccessRole, UnsetType] = unset,
        saml_autocreate_users_domains: Union[OrganizationSettingsSamlAutocreateUsersDomains, UnsetType] = unset,
        saml_can_be_enabled: Union[bool, UnsetType] = unset,
        saml_idp_endpoint: Union[str, UnsetType] = unset,
        saml_idp_initiated_login: Union[OrganizationSettingsSamlIdpInitiatedLogin, UnsetType] = unset,
        saml_idp_metadata_uploaded: Union[bool, UnsetType] = unset,
        saml_login_url: Union[str, UnsetType] = unset,
        saml_strict_mode: Union[OrganizationSettingsSamlStrictMode, UnsetType] = unset,
        **kwargs,
    ):
        """
        A JSON array of settings.

        :param private_widget_share: Whether or not the organization users can share widgets outside of Datadog.
        :type private_widget_share: bool, optional

        :param saml: Set the boolean property enabled to enable or disable single sign on with SAML.
            See the SAML documentation for more information about all SAML settings.
        :type saml: OrganizationSettingsSaml, optional

        :param saml_autocreate_access_role: The access role of the user. Options are **st** (standard user), **adm** (admin user), or **ro** (read-only user).
        :type saml_autocreate_access_role: AccessRole, optional

        :param saml_autocreate_users_domains: Has two properties, ``enabled`` (boolean) and ``domains`` , which is a list of domains without the @ symbol.
        :type saml_autocreate_users_domains: OrganizationSettingsSamlAutocreateUsersDomains, optional

        :param saml_can_be_enabled: Whether or not SAML can be enabled for this organization.
        :type saml_can_be_enabled: bool, optional

        :param saml_idp_endpoint: Identity provider endpoint for SAML authentication.
        :type saml_idp_endpoint: str, optional

        :param saml_idp_initiated_login: Has one property enabled (boolean).
        :type saml_idp_initiated_login: OrganizationSettingsSamlIdpInitiatedLogin, optional

        :param saml_idp_metadata_uploaded: Whether or not a SAML identity provider metadata file was provided to the Datadog organization.
        :type saml_idp_metadata_uploaded: bool, optional

        :param saml_login_url: URL for SAML logging.
        :type saml_login_url: str, optional

        :param saml_strict_mode: Has one property enabled (boolean).
        :type saml_strict_mode: OrganizationSettingsSamlStrictMode, optional
        """
        if private_widget_share is not unset:
            kwargs["private_widget_share"] = private_widget_share
        if saml is not unset:
            kwargs["saml"] = saml
        if saml_autocreate_access_role is not unset:
            kwargs["saml_autocreate_access_role"] = saml_autocreate_access_role
        if saml_autocreate_users_domains is not unset:
            kwargs["saml_autocreate_users_domains"] = saml_autocreate_users_domains
        if saml_can_be_enabled is not unset:
            kwargs["saml_can_be_enabled"] = saml_can_be_enabled
        if saml_idp_endpoint is not unset:
            kwargs["saml_idp_endpoint"] = saml_idp_endpoint
        if saml_idp_initiated_login is not unset:
            kwargs["saml_idp_initiated_login"] = saml_idp_initiated_login
        if saml_idp_metadata_uploaded is not unset:
            kwargs["saml_idp_metadata_uploaded"] = saml_idp_metadata_uploaded
        if saml_login_url is not unset:
            kwargs["saml_login_url"] = saml_login_url
        if saml_strict_mode is not unset:
            kwargs["saml_strict_mode"] = saml_strict_mode
        super().__init__(kwargs)
