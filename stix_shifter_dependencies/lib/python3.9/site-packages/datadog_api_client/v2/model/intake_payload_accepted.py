# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import List, Union

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
            "errors": ([str],),
        }

    attribute_map = {
        "errors": "errors",
    }

    def __init__(self_, errors: Union[List[str], UnsetType] = unset, **kwargs):
        """
        The payload accepted for intake.

        :param errors: A list of errors.
        :type errors: [str], optional
        """
        if errors is not unset:
            kwargs["errors"] = errors
        super().__init__(kwargs)
