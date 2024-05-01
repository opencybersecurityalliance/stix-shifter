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
    from datadog_api_client.v2.model.rum_application import RUMApplication


class RUMApplicationResponse(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.rum_application import RUMApplication

        return {
            "data": (RUMApplication,),
        }

    attribute_map = {
        "data": "data",
    }

    def __init__(self_, data: Union[RUMApplication, UnsetType] = unset, **kwargs):
        """
        RUM application response.

        :param data: RUM application.
        :type data: RUMApplication, optional
        """
        if data is not unset:
            kwargs["data"] = data
        super().__init__(kwargs)
