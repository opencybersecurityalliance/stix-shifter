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
    from datadog_api_client.v1.model.service_level_objective import ServiceLevelObjective
    from datadog_api_client.v1.model.slo_list_response_metadata import SLOListResponseMetadata


class SLOListResponse(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.service_level_objective import ServiceLevelObjective
        from datadog_api_client.v1.model.slo_list_response_metadata import SLOListResponseMetadata

        return {
            "data": ([ServiceLevelObjective],),
            "errors": ([str],),
            "metadata": (SLOListResponseMetadata,),
        }

    attribute_map = {
        "data": "data",
        "errors": "errors",
        "metadata": "metadata",
    }

    def __init__(
        self_,
        data: Union[List[ServiceLevelObjective], UnsetType] = unset,
        errors: Union[List[str], UnsetType] = unset,
        metadata: Union[SLOListResponseMetadata, UnsetType] = unset,
        **kwargs,
    ):
        """
        A response with one or more service level objective.

        :param data: An array of service level objective objects.
        :type data: [ServiceLevelObjective], optional

        :param errors: An array of error messages. Each endpoint documents how/whether this field is
            used.
        :type errors: [str], optional

        :param metadata: The metadata object containing additional information about the list of SLOs.
        :type metadata: SLOListResponseMetadata, optional
        """
        if data is not unset:
            kwargs["data"] = data
        if errors is not unset:
            kwargs["errors"] = errors
        if metadata is not unset:
            kwargs["metadata"] = metadata
        super().__init__(kwargs)
