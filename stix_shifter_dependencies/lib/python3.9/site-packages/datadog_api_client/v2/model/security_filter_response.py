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
    from datadog_api_client.v2.model.security_filter import SecurityFilter
    from datadog_api_client.v2.model.security_filter_meta import SecurityFilterMeta


class SecurityFilterResponse(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.security_filter import SecurityFilter
        from datadog_api_client.v2.model.security_filter_meta import SecurityFilterMeta

        return {
            "data": (SecurityFilter,),
            "meta": (SecurityFilterMeta,),
        }

    attribute_map = {
        "data": "data",
        "meta": "meta",
    }

    def __init__(
        self_,
        data: Union[SecurityFilter, UnsetType] = unset,
        meta: Union[SecurityFilterMeta, UnsetType] = unset,
        **kwargs,
    ):
        """
        Response object which includes a single security filter.

        :param data: The security filter's properties.
        :type data: SecurityFilter, optional

        :param meta: Optional metadata associated to the response.
        :type meta: SecurityFilterMeta, optional
        """
        if data is not unset:
            kwargs["data"] = data
        if meta is not unset:
            kwargs["meta"] = meta
        super().__init__(kwargs)
