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
    from datadog_api_client.v1.model.search_slo_response_data_attributes import SearchSLOResponseDataAttributes


class SearchSLOResponseData(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.search_slo_response_data_attributes import SearchSLOResponseDataAttributes

        return {
            "attributes": (SearchSLOResponseDataAttributes,),
            "type": (str,),
        }

    attribute_map = {
        "attributes": "attributes",
        "type": "type",
    }

    def __init__(
        self_,
        attributes: Union[SearchSLOResponseDataAttributes, UnsetType] = unset,
        type: Union[str, UnsetType] = unset,
        **kwargs,
    ):
        """
        Data from search SLO response.

        :param attributes: Attributes
        :type attributes: SearchSLOResponseDataAttributes, optional

        :param type: Type of service level objective result.
        :type type: str, optional
        """
        if attributes is not unset:
            kwargs["attributes"] = attributes
        if type is not unset:
            kwargs["type"] = type
        super().__init__(kwargs)
