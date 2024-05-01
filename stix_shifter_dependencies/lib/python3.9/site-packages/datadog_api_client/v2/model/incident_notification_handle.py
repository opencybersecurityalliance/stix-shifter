# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Union

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    unset,
    UnsetType,
)


class IncidentNotificationHandle(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "display_name": (str,),
            "handle": (str,),
        }

    attribute_map = {
        "display_name": "display_name",
        "handle": "handle",
    }

    def __init__(self_, display_name: Union[str, UnsetType] = unset, handle: Union[str, UnsetType] = unset, **kwargs):
        """
        A notification handle that will be notified at incident creation.

        :param display_name: The name of the notified handle.
        :type display_name: str, optional

        :param handle: The email address used for the notification.
        :type handle: str, optional
        """
        if display_name is not unset:
            kwargs["display_name"] = display_name
        if handle is not unset:
            kwargs["handle"] = handle
        super().__init__(kwargs)
