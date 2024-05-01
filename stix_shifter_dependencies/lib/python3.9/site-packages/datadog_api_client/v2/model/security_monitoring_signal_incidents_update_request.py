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
    from datadog_api_client.v2.model.security_monitoring_signal_incidents_update_data import (
        SecurityMonitoringSignalIncidentsUpdateData,
    )


class SecurityMonitoringSignalIncidentsUpdateRequest(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.security_monitoring_signal_incidents_update_data import (
            SecurityMonitoringSignalIncidentsUpdateData,
        )

        return {
            "data": (SecurityMonitoringSignalIncidentsUpdateData,),
        }

    attribute_map = {
        "data": "data",
    }

    def __init__(self_, data: SecurityMonitoringSignalIncidentsUpdateData, **kwargs):
        """
        Request body for changing the related incidents of a given security monitoring signal.

        :param data: Data containing the patch for changing the related incidents of a signal.
        :type data: SecurityMonitoringSignalIncidentsUpdateData
        """
        super().__init__(kwargs)

        self_.data = data
