# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Union, TYPE_CHECKING

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    none_type,
    unset,
    UnsetType,
)


if TYPE_CHECKING:
    from datadog_api_client.v1.model.slo_correction_category import SLOCorrectionCategory
    from datadog_api_client.v1.model.creator import Creator
    from datadog_api_client.v1.model.slo_correction_response_attributes_modifier import (
        SLOCorrectionResponseAttributesModifier,
    )


class SLOCorrectionResponseAttributes(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.slo_correction_category import SLOCorrectionCategory
        from datadog_api_client.v1.model.creator import Creator
        from datadog_api_client.v1.model.slo_correction_response_attributes_modifier import (
            SLOCorrectionResponseAttributesModifier,
        )

        return {
            "category": (SLOCorrectionCategory,),
            "created_at": (int, none_type),
            "creator": (Creator,),
            "description": (str,),
            "duration": (int, none_type),
            "end": (int, none_type),
            "modified_at": (int, none_type),
            "modifier": (SLOCorrectionResponseAttributesModifier,),
            "rrule": (str, none_type),
            "slo_id": (str,),
            "start": (int,),
            "timezone": (str,),
        }

    attribute_map = {
        "category": "category",
        "created_at": "created_at",
        "creator": "creator",
        "description": "description",
        "duration": "duration",
        "end": "end",
        "modified_at": "modified_at",
        "modifier": "modifier",
        "rrule": "rrule",
        "slo_id": "slo_id",
        "start": "start",
        "timezone": "timezone",
    }
    read_only_vars = {
        "creator",
    }

    def __init__(
        self_,
        category: Union[SLOCorrectionCategory, UnsetType] = unset,
        created_at: Union[int, none_type, UnsetType] = unset,
        creator: Union[Creator, UnsetType] = unset,
        description: Union[str, UnsetType] = unset,
        duration: Union[int, none_type, UnsetType] = unset,
        end: Union[int, none_type, UnsetType] = unset,
        modified_at: Union[int, none_type, UnsetType] = unset,
        modifier: Union[SLOCorrectionResponseAttributesModifier, none_type, UnsetType] = unset,
        rrule: Union[str, none_type, UnsetType] = unset,
        slo_id: Union[str, UnsetType] = unset,
        start: Union[int, UnsetType] = unset,
        timezone: Union[str, UnsetType] = unset,
        **kwargs,
    ):
        """
        The attribute object associated with the SLO correction.

        :param category: Category the SLO correction belongs to.
        :type category: SLOCorrectionCategory, optional

        :param created_at: The epoch timestamp of when the correction was created at.
        :type created_at: int, none_type, optional

        :param creator: Object describing the creator of the shared element.
        :type creator: Creator, optional

        :param description: Description of the correction being made.
        :type description: str, optional

        :param duration: Length of time (in seconds) for a specified ``rrule`` recurring SLO correction.
        :type duration: int, none_type, optional

        :param end: Ending time of the correction in epoch seconds.
        :type end: int, none_type, optional

        :param modified_at: The epoch timestamp of when the correction was modified at.
        :type modified_at: int, none_type, optional

        :param modifier: Modifier of the object.
        :type modifier: SLOCorrectionResponseAttributesModifier, none_type, optional

        :param rrule: The recurrence rules as defined in the iCalendar RFC 5545. The supported rules for SLO corrections
            are ``FREQ`` , ``INTERVAL`` , ``COUNT`` , and ``UNTIL``.
        :type rrule: str, none_type, optional

        :param slo_id: ID of the SLO that this correction applies to.
        :type slo_id: str, optional

        :param start: Starting time of the correction in epoch seconds.
        :type start: int, optional

        :param timezone: The timezone to display in the UI for the correction times (defaults to "UTC").
        :type timezone: str, optional
        """
        if category is not unset:
            kwargs["category"] = category
        if created_at is not unset:
            kwargs["created_at"] = created_at
        if creator is not unset:
            kwargs["creator"] = creator
        if description is not unset:
            kwargs["description"] = description
        if duration is not unset:
            kwargs["duration"] = duration
        if end is not unset:
            kwargs["end"] = end
        if modified_at is not unset:
            kwargs["modified_at"] = modified_at
        if modifier is not unset:
            kwargs["modifier"] = modifier
        if rrule is not unset:
            kwargs["rrule"] = rrule
        if slo_id is not unset:
            kwargs["slo_id"] = slo_id
        if start is not unset:
            kwargs["start"] = start
        if timezone is not unset:
            kwargs["timezone"] = timezone
        super().__init__(kwargs)
