# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import TYPE_CHECKING

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
)


if TYPE_CHECKING:
    from datadog_api_client.v1.model.notebook_create_data import NotebookCreateData


class NotebookCreateRequest(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.notebook_create_data import NotebookCreateData

        return {
            "data": (NotebookCreateData,),
        }

    attribute_map = {
        "data": "data",
    }

    def __init__(self_, data: NotebookCreateData, **kwargs):
        """
        The description of a notebook create request.

        :param data: The data for a notebook create request.
        :type data: NotebookCreateData
        """
        super().__init__(kwargs)

        self_.data = data
