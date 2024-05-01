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


class AWSLogsListServicesResponse(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "id": (str,),
            "label": (str,),
        }

    attribute_map = {
        "id": "id",
        "label": "label",
    }

    def __init__(self_, id: Union[str, UnsetType] = unset, label: Union[str, UnsetType] = unset, **kwargs):
        """
        The list of current AWS services for which Datadog offers automatic log collection.

        :param id: Key value in returned object.
        :type id: str, optional

        :param label: Name of service available for configuration with Datadog logs.
        :type label: str, optional
        """
        if id is not unset:
            kwargs["id"] = id
        if label is not unset:
            kwargs["label"] = label
        super().__init__(kwargs)
