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
    from datadog_api_client.v1.model.synthetics_restricted_roles import SyntheticsRestrictedRoles


class SyntheticsGlobalVariableAttributes(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.synthetics_restricted_roles import SyntheticsRestrictedRoles

        return {
            "restricted_roles": (SyntheticsRestrictedRoles,),
        }

    attribute_map = {
        "restricted_roles": "restricted_roles",
    }

    def __init__(self_, restricted_roles: Union[SyntheticsRestrictedRoles, UnsetType] = unset, **kwargs):
        """
        Attributes of the global variable.

        :param restricted_roles: A list of role identifiers that can be pulled from the Roles API, for restricting read and write access.
        :type restricted_roles: SyntheticsRestrictedRoles, optional
        """
        if restricted_roles is not unset:
            kwargs["restricted_roles"] = restricted_roles
        super().__init__(kwargs)
