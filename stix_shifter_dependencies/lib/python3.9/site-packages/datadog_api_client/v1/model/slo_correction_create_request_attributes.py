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
    from datadog_api_client.v1.model.slo_correction_category import SLOCorrectionCategory


class SLOCorrectionCreateRequestAttributes(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.slo_correction_category import SLOCorrectionCategory

        return {
            "category": (SLOCorrectionCategory,),
            "description": (str,),
            "duration": (int,),
            "end": (int,),
            "rrule": (str,),
            "slo_id": (str,),
            "start": (int,),
            "timezone": (str,),
        }

    attribute_map = {
        "category": "category",
        "description": "description",
        "duration": "duration",
        "end": "end",
        "rrule": "rrule",
        "slo_id": "slo_id",
        "start": "start",
        "timezone": "timezone",
    }

    def __init__(
        self_,
        category: SLOCorrectionCategory,
        slo_id: str,
        start: int,
        description: Union[str, UnsetType] = unset,
        duration: Union[int, UnsetType] = unset,
        end: Union[int, UnsetType] = unset,
        rrule: Union[str, UnsetType] = unset,
        timezone: Union[str, UnsetType] = unset,
        **kwargs,
    ):
        """
        The attribute object associated with the SLO correction to be created.

        :param category: Category the SLO correction belongs to.
        :type category: SLOCorrectionCategory

        :param description: Description of the correction being made.
        :type description: str, optional

        :param duration: Length of time (in seconds) for a specified ``rrule`` recurring SLO correction.
        :type duration: int, optional

        :param end: Ending time of the correction in epoch seconds.
        :type end: int, optional

        :param rrule: The recurrence rules as defined in the iCalendar RFC 5545. The supported rules for SLO corrections
            are ``FREQ`` , ``INTERVAL`` , ``COUNT`` and ``UNTIL``.
        :type rrule: str, optional

        :param slo_id: ID of the SLO that this correction applies to.
        :type slo_id: str

        :param start: Starting time of the correction in epoch seconds.
        :type start: int

        :param timezone: The timezone to display in the UI for the correction times (defaults to "UTC").
        :type timezone: str, optional
        """
        if description is not unset:
            kwargs["description"] = description
        if duration is not unset:
            kwargs["duration"] = duration
        if end is not unset:
            kwargs["end"] = end
        if rrule is not unset:
            kwargs["rrule"] = rrule
        if timezone is not unset:
            kwargs["timezone"] = timezone
        super().__init__(kwargs)

        self_.category = category
        self_.slo_id = slo_id
        self_.start = start
