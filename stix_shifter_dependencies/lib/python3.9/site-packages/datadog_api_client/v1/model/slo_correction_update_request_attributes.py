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


class SLOCorrectionUpdateRequestAttributes(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.slo_correction_category import SLOCorrectionCategory

        return {
            "category": (SLOCorrectionCategory,),
            "description": (str,),
            "duration": (int,),
            "end": (int,),
            "rrule": (str,),
            "start": (int,),
            "timezone": (str,),
        }

    attribute_map = {
        "category": "category",
        "description": "description",
        "duration": "duration",
        "end": "end",
        "rrule": "rrule",
        "start": "start",
        "timezone": "timezone",
    }

    def __init__(
        self_,
        category: Union[SLOCorrectionCategory, UnsetType] = unset,
        description: Union[str, UnsetType] = unset,
        duration: Union[int, UnsetType] = unset,
        end: Union[int, UnsetType] = unset,
        rrule: Union[str, UnsetType] = unset,
        start: Union[int, UnsetType] = unset,
        timezone: Union[str, UnsetType] = unset,
        **kwargs,
    ):
        """
        The attribute object associated with the SLO correction to be updated.

        :param category: Category the SLO correction belongs to.
        :type category: SLOCorrectionCategory, optional

        :param description: Description of the correction being made.
        :type description: str, optional

        :param duration: Length of time (in seconds) for a specified ``rrule`` recurring SLO correction.
        :type duration: int, optional

        :param end: Ending time of the correction in epoch seconds.
        :type end: int, optional

        :param rrule: The recurrence rules as defined in the iCalendar RFC 5545. The supported rules for SLO corrections
            are ``FREQ`` , ``INTERVAL`` , ``COUNT`` , and ``UNTIL``.
        :type rrule: str, optional

        :param start: Starting time of the correction in epoch seconds.
        :type start: int, optional

        :param timezone: The timezone to display in the UI for the correction times (defaults to "UTC").
        :type timezone: str, optional
        """
        if category is not unset:
            kwargs["category"] = category
        if description is not unset:
            kwargs["description"] = description
        if duration is not unset:
            kwargs["duration"] = duration
        if end is not unset:
            kwargs["end"] = end
        if rrule is not unset:
            kwargs["rrule"] = rrule
        if start is not unset:
            kwargs["start"] = start
        if timezone is not unset:
            kwargs["timezone"] = timezone
        super().__init__(kwargs)
