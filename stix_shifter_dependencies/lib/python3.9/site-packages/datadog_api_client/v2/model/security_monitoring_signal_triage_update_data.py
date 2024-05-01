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
    from datadog_api_client.v2.model.security_monitoring_signal_triage_attributes import (
        SecurityMonitoringSignalTriageAttributes,
    )


class SecurityMonitoringSignalTriageUpdateData(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.security_monitoring_signal_triage_attributes import (
            SecurityMonitoringSignalTriageAttributes,
        )

        return {
            "attributes": (SecurityMonitoringSignalTriageAttributes,),
        }

    attribute_map = {
        "attributes": "attributes",
    }

    def __init__(self_, attributes: Union[SecurityMonitoringSignalTriageAttributes, UnsetType] = unset, **kwargs):
        """
        Data containing the updated triage attributes of the signal.

        :param attributes: Attributes describing a triage state update operation over a security signal.
        :type attributes: SecurityMonitoringSignalTriageAttributes, optional
        """
        if attributes is not unset:
            kwargs["attributes"] = attributes
        super().__init__(kwargs)
