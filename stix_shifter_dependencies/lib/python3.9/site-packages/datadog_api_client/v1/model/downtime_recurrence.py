# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import List, Union

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    none_type,
    unset,
    UnsetType,
)


class DowntimeRecurrence(ModelNormal):
    validations = {
        "period": {
            "inclusive_maximum": 2147483647,
        },
        "until_occurrences": {
            "inclusive_maximum": 2147483647,
        },
    }
    _nullable = True

    @cached_property
    def openapi_types(_):
        return {
            "period": (int,),
            "rrule": (str,),
            "type": (str,),
            "until_date": (int, none_type),
            "until_occurrences": (int, none_type),
            "week_days": ([str], none_type),
        }

    attribute_map = {
        "period": "period",
        "rrule": "rrule",
        "type": "type",
        "until_date": "until_date",
        "until_occurrences": "until_occurrences",
        "week_days": "week_days",
    }

    def __init__(
        self_,
        period: Union[int, UnsetType] = unset,
        rrule: Union[str, UnsetType] = unset,
        type: Union[str, UnsetType] = unset,
        until_date: Union[int, none_type, UnsetType] = unset,
        until_occurrences: Union[int, none_type, UnsetType] = unset,
        week_days: Union[List[str], none_type, UnsetType] = unset,
        **kwargs,
    ):
        """
        An object defining the recurrence of the downtime.

        :param period: How often to repeat as an integer.
            For example, to repeat every 3 days, select a type of ``days`` and a period of ``3``.
        :type period: int, optional

        :param rrule: The ``RRULE`` standard for defining recurring events ( **requires to set "type" to rrule** )
            For example, to have a recurring event on the first day of each month, set the type to ``rrule`` and set the ``FREQ`` to ``MONTHLY`` and ``BYMONTHDAY`` to ``1``.
            Most common ``rrule`` options from the `iCalendar Spec <https://tools.ietf.org/html/rfc5545>`_ are supported.

            **Note** : Attributes specifying the duration in ``RRULE`` are not supported (for example, ``DTSTART`` , ``DTEND`` , ``DURATION`` ).
            More examples available in this `downtime guide <https://docs.datadoghq.com/monitors/guide/suppress-alert-with-downtimes/?tab=api>`_
        :type rrule: str, optional

        :param type: The type of recurrence. Choose from ``days`` , ``weeks`` , ``months`` , ``years`` , ``rrule``.
        :type type: str, optional

        :param until_date: The date at which the recurrence should end as a POSIX timestamp.
            ``until_occurences`` and ``until_date`` are mutually exclusive.
        :type until_date: int, none_type, optional

        :param until_occurrences: How many times the downtime is rescheduled.
            ``until_occurences`` and ``until_date`` are mutually exclusive.
        :type until_occurrences: int, none_type, optional

        :param week_days: A list of week days to repeat on. Choose from ``Mon`` , ``Tue`` , ``Wed`` , ``Thu`` , ``Fri`` , ``Sat`` or ``Sun``.
            Only applicable when type is weeks. First letter must be capitalized.
        :type week_days: [str], none_type, optional
        """
        if period is not unset:
            kwargs["period"] = period
        if rrule is not unset:
            kwargs["rrule"] = rrule
        if type is not unset:
            kwargs["type"] = type
        if until_date is not unset:
            kwargs["until_date"] = until_date
        if until_occurrences is not unset:
            kwargs["until_occurrences"] = until_occurrences
        if week_days is not unset:
            kwargs["week_days"] = week_days
        super().__init__(kwargs)
