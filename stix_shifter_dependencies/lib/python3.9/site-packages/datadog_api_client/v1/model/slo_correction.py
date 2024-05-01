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
    from datadog_api_client.v1.model.slo_correction_response_attributes import SLOCorrectionResponseAttributes
    from datadog_api_client.v1.model.slo_correction_type import SLOCorrectionType


class SLOCorrection(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.slo_correction_response_attributes import SLOCorrectionResponseAttributes
        from datadog_api_client.v1.model.slo_correction_type import SLOCorrectionType

        return {
            "attributes": (SLOCorrectionResponseAttributes,),
            "id": (str,),
            "type": (SLOCorrectionType,),
        }

    attribute_map = {
        "attributes": "attributes",
        "id": "id",
        "type": "type",
    }

    def __init__(
        self_,
        attributes: Union[SLOCorrectionResponseAttributes, UnsetType] = unset,
        id: Union[str, UnsetType] = unset,
        type: Union[SLOCorrectionType, UnsetType] = unset,
        **kwargs,
    ):
        """
        The response object of a list of SLO corrections.

        :param attributes: The attribute object associated with the SLO correction.
        :type attributes: SLOCorrectionResponseAttributes, optional

        :param id: The ID of the SLO correction.
        :type id: str, optional

        :param type: SLO correction resource type.
        :type type: SLOCorrectionType, optional
        """
        if attributes is not unset:
            kwargs["attributes"] = attributes
        if id is not unset:
            kwargs["id"] = id
        if type is not unset:
            kwargs["type"] = type
        super().__init__(kwargs)
