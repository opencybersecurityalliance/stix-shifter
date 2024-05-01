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


class AddSignalToIncidentRequest(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "add_to_signal_timeline": (bool,),
            "incident_id": (int,),
            "version": (int,),
        }

    attribute_map = {
        "add_to_signal_timeline": "add_to_signal_timeline",
        "incident_id": "incident_id",
        "version": "version",
    }

    def __init__(
        self_,
        incident_id: int,
        add_to_signal_timeline: Union[bool, UnsetType] = unset,
        version: Union[int, UnsetType] = unset,
        **kwargs,
    ):
        """
        Attributes describing which incident to add the signal to.

        :param add_to_signal_timeline: Whether to post the signal on the incident timeline.
        :type add_to_signal_timeline: bool, optional

        :param incident_id: Public ID attribute of the incident to which the signal will be added.
        :type incident_id: int

        :param version: Version of the updated signal. If server side version is higher, update will be rejected.
        :type version: int, optional
        """
        if add_to_signal_timeline is not unset:
            kwargs["add_to_signal_timeline"] = add_to_signal_timeline
        if version is not unset:
            kwargs["version"] = version
        super().__init__(kwargs)

        self_.incident_id = incident_id
