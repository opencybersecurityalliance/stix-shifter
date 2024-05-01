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
    from datadog_api_client.v2.model.incident_response_meta_pagination import IncidentResponseMetaPagination


class IncidentSearchResponseMeta(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.incident_response_meta_pagination import IncidentResponseMetaPagination

        return {
            "pagination": (IncidentResponseMetaPagination,),
        }

    attribute_map = {
        "pagination": "pagination",
    }

    def __init__(self_, pagination: Union[IncidentResponseMetaPagination, UnsetType] = unset, **kwargs):
        """
        The metadata object containing pagination metadata.

        :param pagination: Pagination properties.
        :type pagination: IncidentResponseMetaPagination, optional
        """
        if pagination is not unset:
            kwargs["pagination"] = pagination
        super().__init__(kwargs)
