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
    from datadog_api_client.v1.model.aws_logs_async_error import AWSLogsAsyncError


class AWSLogsAsyncResponse(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.aws_logs_async_error import AWSLogsAsyncError

        return {
            "errors": ([AWSLogsAsyncError],),
            "status": (str,),
        }

    attribute_map = {
        "errors": "errors",
        "status": "status",
    }

    def __init__(
        self_,
        errors: Union[List[AWSLogsAsyncError], UnsetType] = unset,
        status: Union[str, UnsetType] = unset,
        **kwargs,
    ):
        """
        A list of all Datadog-AWS logs integrations available in your Datadog organization.

        :param errors: List of errors.
        :type errors: [AWSLogsAsyncError], optional

        :param status: Status of the properties.
        :type status: str, optional
        """
        if errors is not unset:
            kwargs["errors"] = errors
        if status is not unset:
            kwargs["status"] = status
        super().__init__(kwargs)
