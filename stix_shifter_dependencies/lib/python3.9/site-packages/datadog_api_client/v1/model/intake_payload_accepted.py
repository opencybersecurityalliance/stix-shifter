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


class IntakePayloadAccepted(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "status": (str,),
        }

    attribute_map = {
        "status": "status",
    }

    def __init__(self_, status: Union[str, UnsetType] = unset, **kwargs):
        """
        The payload accepted for intake.

        :param status: The status of the intake payload.
        :type status: str, optional
        """
        if status is not unset:
            kwargs["status"] = status
        super().__init__(kwargs)
