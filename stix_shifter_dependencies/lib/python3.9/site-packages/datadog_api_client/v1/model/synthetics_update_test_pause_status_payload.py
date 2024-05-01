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
    from datadog_api_client.v1.model.synthetics_test_pause_status import SyntheticsTestPauseStatus


class SyntheticsUpdateTestPauseStatusPayload(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.synthetics_test_pause_status import SyntheticsTestPauseStatus

        return {
            "new_status": (SyntheticsTestPauseStatus,),
        }

    attribute_map = {
        "new_status": "new_status",
    }

    def __init__(self_, new_status: Union[SyntheticsTestPauseStatus, UnsetType] = unset, **kwargs):
        """
        Object to start or pause an existing Synthetic test.

        :param new_status: Define whether you want to start ( ``live`` ) or pause ( ``paused`` ) a
            Synthetic test.
        :type new_status: SyntheticsTestPauseStatus, optional
        """
        if new_status is not unset:
            kwargs["new_status"] = new_status
        super().__init__(kwargs)
