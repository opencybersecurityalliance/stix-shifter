# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import List, Union, TYPE_CHECKING

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    unset,
    UnsetType,
)


if TYPE_CHECKING:
    from datadog_api_client.v1.model.organization import Organization


class OrganizationListResponse(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.organization import Organization

        return {
            "orgs": ([Organization],),
        }

    attribute_map = {
        "orgs": "orgs",
    }

    def __init__(self_, orgs: Union[List[Organization], UnsetType] = unset, **kwargs):
        """
        Response with the list of organizations.

        :param orgs: Array of organization objects.
        :type orgs: [Organization], optional
        """
        if orgs is not unset:
            kwargs["orgs"] = orgs
        super().__init__(kwargs)
