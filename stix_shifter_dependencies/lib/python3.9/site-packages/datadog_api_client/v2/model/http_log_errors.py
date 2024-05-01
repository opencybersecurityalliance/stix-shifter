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
    from datadog_api_client.v2.model.http_log_error import HTTPLogError


class HTTPLogErrors(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.http_log_error import HTTPLogError

        return {
            "errors": ([HTTPLogError],),
        }

    attribute_map = {
        "errors": "errors",
    }

    def __init__(self_, errors: Union[List[HTTPLogError], UnsetType] = unset, **kwargs):
        """
        Invalid query performed.

        :param errors: Structured errors.
        :type errors: [HTTPLogError], optional
        """
        if errors is not unset:
            kwargs["errors"] = errors
        super().__init__(kwargs)
