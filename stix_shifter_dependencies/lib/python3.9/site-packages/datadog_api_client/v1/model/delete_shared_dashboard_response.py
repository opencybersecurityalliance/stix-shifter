# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Union

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    unset,
    UnsetType,
)


class DeleteSharedDashboardResponse(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "deleted_public_dashboard_token": (str,),
        }

    attribute_map = {
        "deleted_public_dashboard_token": "deleted_public_dashboard_token",
    }

    def __init__(self_, deleted_public_dashboard_token: Union[str, UnsetType] = unset, **kwargs):
        """
        Response containing token of deleted shared dashboard.

        :param deleted_public_dashboard_token: Token associated with the shared dashboard that was revoked.
        :type deleted_public_dashboard_token: str, optional
        """
        if deleted_public_dashboard_token is not unset:
            kwargs["deleted_public_dashboard_token"] = deleted_public_dashboard_token
        super().__init__(kwargs)
