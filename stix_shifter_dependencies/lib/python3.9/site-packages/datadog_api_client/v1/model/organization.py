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
    from datadog_api_client.v1.model.organization_billing import OrganizationBilling
    from datadog_api_client.v1.model.organization_settings import OrganizationSettings
    from datadog_api_client.v1.model.organization_subscription import OrganizationSubscription


class Organization(ModelNormal):
    validations = {
        "name": {
            "max_length": 32,
        },
    }

    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.organization_billing import OrganizationBilling
        from datadog_api_client.v1.model.organization_settings import OrganizationSettings
        from datadog_api_client.v1.model.organization_subscription import OrganizationSubscription

        return {
            "billing": (OrganizationBilling,),
            "created": (str,),
            "description": (str,),
            "name": (str,),
            "public_id": (str,),
            "settings": (OrganizationSettings,),
            "subscription": (OrganizationSubscription,),
            "trial": (bool,),
        }

    attribute_map = {
        "billing": "billing",
        "created": "created",
        "description": "description",
        "name": "name",
        "public_id": "public_id",
        "settings": "settings",
        "subscription": "subscription",
        "trial": "trial",
    }
    read_only_vars = {
        "created",
    }

    def __init__(
        self_,
        billing: Union[OrganizationBilling, UnsetType] = unset,
        created: Union[str, UnsetType] = unset,
        description: Union[str, UnsetType] = unset,
        name: Union[str, UnsetType] = unset,
        public_id: Union[str, UnsetType] = unset,
        settings: Union[OrganizationSettings, UnsetType] = unset,
        subscription: Union[OrganizationSubscription, UnsetType] = unset,
        trial: Union[bool, UnsetType] = unset,
        **kwargs,
    ):
        """
        Create, edit, and manage organizations.

        :param billing: A JSON array of billing type. **Deprecated**.
        :type billing: OrganizationBilling, optional

        :param created: Date of the organization creation.
        :type created: str, optional

        :param description: Description of the organization.
        :type description: str, optional

        :param name: The name of the new child-organization, limited to 32 characters.
        :type name: str, optional

        :param public_id: The ``public_id`` of the organization you are operating within.
        :type public_id: str, optional

        :param settings: A JSON array of settings.
        :type settings: OrganizationSettings, optional

        :param subscription: Subscription definition. **Deprecated**.
        :type subscription: OrganizationSubscription, optional

        :param trial: Only available for MSP customers. Allows child organizations to be created on a trial plan.
        :type trial: bool, optional
        """
        if billing is not unset:
            kwargs["billing"] = billing
        if created is not unset:
            kwargs["created"] = created
        if description is not unset:
            kwargs["description"] = description
        if name is not unset:
            kwargs["name"] = name
        if public_id is not unset:
            kwargs["public_id"] = public_id
        if settings is not unset:
            kwargs["settings"] = settings
        if subscription is not unset:
            kwargs["subscription"] = subscription
        if trial is not unset:
            kwargs["trial"] = trial
        super().__init__(kwargs)
