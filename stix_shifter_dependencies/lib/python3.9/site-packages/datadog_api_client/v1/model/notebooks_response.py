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
    from datadog_api_client.v1.model.notebooks_response_data import NotebooksResponseData
    from datadog_api_client.v1.model.notebooks_response_meta import NotebooksResponseMeta


class NotebooksResponse(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.notebooks_response_data import NotebooksResponseData
        from datadog_api_client.v1.model.notebooks_response_meta import NotebooksResponseMeta

        return {
            "data": ([NotebooksResponseData],),
            "meta": (NotebooksResponseMeta,),
        }

    attribute_map = {
        "data": "data",
        "meta": "meta",
    }

    def __init__(
        self_,
        data: Union[List[NotebooksResponseData], UnsetType] = unset,
        meta: Union[NotebooksResponseMeta, UnsetType] = unset,
        **kwargs,
    ):
        """
        Notebooks get all response.

        :param data: List of notebook definitions.
        :type data: [NotebooksResponseData], optional

        :param meta: Searches metadata returned by the API.
        :type meta: NotebooksResponseMeta, optional
        """
        if data is not unset:
            kwargs["data"] = data
        if meta is not unset:
            kwargs["meta"] = meta
        super().__init__(kwargs)
