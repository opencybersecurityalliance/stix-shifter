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
    from datadog_api_client.v1.model.synthetics_device_id import SyntheticsDeviceID


class SyntheticsTriggerCITestRunResult(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.synthetics_device_id import SyntheticsDeviceID

        return {
            "device": (SyntheticsDeviceID,),
            "location": (int,),
            "public_id": (str,),
            "result_id": (str,),
        }

    attribute_map = {
        "device": "device",
        "location": "location",
        "public_id": "public_id",
        "result_id": "result_id",
    }

    def __init__(
        self_,
        device: Union[SyntheticsDeviceID, UnsetType] = unset,
        location: Union[int, UnsetType] = unset,
        public_id: Union[str, UnsetType] = unset,
        result_id: Union[str, UnsetType] = unset,
        **kwargs,
    ):
        """
        Information about a single test run.

        :param device: The device ID.
        :type device: SyntheticsDeviceID, optional

        :param location: The location ID of the test run.
        :type location: int, optional

        :param public_id: The public ID of the Synthetics test.
        :type public_id: str, optional

        :param result_id: ID of the result.
        :type result_id: str, optional
        """
        if device is not unset:
            kwargs["device"] = device
        if location is not unset:
            kwargs["location"] = location
        if public_id is not unset:
            kwargs["public_id"] = public_id
        if result_id is not unset:
            kwargs["result_id"] = result_id
        super().__init__(kwargs)
