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
    from datadog_api_client.v2.model.rum_application_create import RUMApplicationCreate


class RUMApplicationCreateRequest(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.rum_application_create import RUMApplicationCreate

        return {
            "data": (RUMApplicationCreate,),
        }

    attribute_map = {
        "data": "data",
    }

    def __init__(self_, data: RUMApplicationCreate, **kwargs):
        """
        RUM application creation request attributes.

        :param data: RUM application creation.
        :type data: RUMApplicationCreate
        """
        super().__init__(kwargs)

        self_.data = data
