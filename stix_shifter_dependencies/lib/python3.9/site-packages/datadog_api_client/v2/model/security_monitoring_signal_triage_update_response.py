# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import TYPE_CHECKING

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
)


if TYPE_CHECKING:
    from datadog_api_client.v2.model.security_monitoring_signal_triage_update_data import (
        SecurityMonitoringSignalTriageUpdateData,
    )


class SecurityMonitoringSignalTriageUpdateResponse(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.security_monitoring_signal_triage_update_data import (
            SecurityMonitoringSignalTriageUpdateData,
        )

        return {
            "data": (SecurityMonitoringSignalTriageUpdateData,),
        }

    attribute_map = {
        "data": "data",
    }

    def __init__(self_, data: SecurityMonitoringSignalTriageUpdateData, **kwargs):
        """
        The response returned after all triage operations, containing the updated signal triage data.

        :param data: Data containing the updated triage attributes of the signal.
        :type data: SecurityMonitoringSignalTriageUpdateData
        """
        super().__init__(kwargs)

        self_.data = data
