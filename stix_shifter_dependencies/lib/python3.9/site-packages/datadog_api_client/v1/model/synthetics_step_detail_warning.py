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
    from datadog_api_client.v1.model.synthetics_warning_type import SyntheticsWarningType


class SyntheticsStepDetailWarning(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.synthetics_warning_type import SyntheticsWarningType

        return {
            "message": (str,),
            "type": (SyntheticsWarningType,),
        }

    attribute_map = {
        "message": "message",
        "type": "type",
    }

    def __init__(self_, message: str, type: SyntheticsWarningType, **kwargs):
        """
        Object collecting warnings for a given step.

        :param message: Message for the warning.
        :type message: str

        :param type: User locator used.
        :type type: SyntheticsWarningType
        """
        super().__init__(kwargs)

        self_.message = message
        self_.type = type
