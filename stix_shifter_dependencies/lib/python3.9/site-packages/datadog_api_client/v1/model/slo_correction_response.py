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
    from datadog_api_client.v1.model.slo_correction import SLOCorrection


class SLOCorrectionResponse(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.slo_correction import SLOCorrection

        return {
            "data": (SLOCorrection,),
        }

    attribute_map = {
        "data": "data",
    }

    def __init__(self_, data: Union[SLOCorrection, UnsetType] = unset, **kwargs):
        """
        The response object of an SLO correction.

        :param data: The response object of a list of SLO corrections.
        :type data: SLOCorrection, optional
        """
        if data is not unset:
            kwargs["data"] = data
        super().__init__(kwargs)
