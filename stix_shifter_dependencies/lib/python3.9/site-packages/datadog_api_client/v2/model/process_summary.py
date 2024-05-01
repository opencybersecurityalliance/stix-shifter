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
    from datadog_api_client.v2.model.process_summary_attributes import ProcessSummaryAttributes
    from datadog_api_client.v2.model.process_summary_type import ProcessSummaryType


class ProcessSummary(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.process_summary_attributes import ProcessSummaryAttributes
        from datadog_api_client.v2.model.process_summary_type import ProcessSummaryType

        return {
            "attributes": (ProcessSummaryAttributes,),
            "id": (str,),
            "type": (ProcessSummaryType,),
        }

    attribute_map = {
        "attributes": "attributes",
        "id": "id",
        "type": "type",
    }

    def __init__(
        self_,
        attributes: Union[ProcessSummaryAttributes, UnsetType] = unset,
        id: Union[str, UnsetType] = unset,
        type: Union[ProcessSummaryType, UnsetType] = unset,
        **kwargs,
    ):
        """
        Process summary object.

        :param attributes: Attributes for a process summary.
        :type attributes: ProcessSummaryAttributes, optional

        :param id: Process ID.
        :type id: str, optional

        :param type: Type of process summary.
        :type type: ProcessSummaryType, optional
        """
        if attributes is not unset:
            kwargs["attributes"] = attributes
        if id is not unset:
            kwargs["id"] = id
        if type is not unset:
            kwargs["type"] = type
        super().__init__(kwargs)
