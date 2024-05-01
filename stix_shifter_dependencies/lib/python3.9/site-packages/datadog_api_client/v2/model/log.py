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
    from datadog_api_client.v2.model.log_attributes import LogAttributes
    from datadog_api_client.v2.model.log_type import LogType


class Log(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.log_attributes import LogAttributes
        from datadog_api_client.v2.model.log_type import LogType

        return {
            "attributes": (LogAttributes,),
            "id": (str,),
            "type": (LogType,),
        }

    attribute_map = {
        "attributes": "attributes",
        "id": "id",
        "type": "type",
    }

    def __init__(
        self_,
        attributes: Union[LogAttributes, UnsetType] = unset,
        id: Union[str, UnsetType] = unset,
        type: Union[LogType, UnsetType] = unset,
        **kwargs,
    ):
        """
        Object description of a log after being processed and stored by Datadog.

        :param attributes: JSON object containing all log attributes and their associated values.
        :type attributes: LogAttributes, optional

        :param id: Unique ID of the Log.
        :type id: str, optional

        :param type: Type of the event.
        :type type: LogType, optional
        """
        if attributes is not unset:
            kwargs["attributes"] = attributes
        if id is not unset:
            kwargs["id"] = id
        if type is not unset:
            kwargs["type"] = type
        super().__init__(kwargs)
