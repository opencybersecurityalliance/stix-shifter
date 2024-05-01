# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Union

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    none_type,
    unset,
    UnsetType,
)


class MonitorThresholds(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "critical": (float,),
            "critical_recovery": (float, none_type),
            "ok": (float, none_type),
            "unknown": (float, none_type),
            "warning": (float, none_type),
            "warning_recovery": (float, none_type),
        }

    attribute_map = {
        "critical": "critical",
        "critical_recovery": "critical_recovery",
        "ok": "ok",
        "unknown": "unknown",
        "warning": "warning",
        "warning_recovery": "warning_recovery",
    }

    def __init__(
        self_,
        critical: Union[float, UnsetType] = unset,
        critical_recovery: Union[float, none_type, UnsetType] = unset,
        ok: Union[float, none_type, UnsetType] = unset,
        unknown: Union[float, none_type, UnsetType] = unset,
        warning: Union[float, none_type, UnsetType] = unset,
        warning_recovery: Union[float, none_type, UnsetType] = unset,
        **kwargs,
    ):
        """
        List of the different monitor threshold available.

        :param critical: The monitor ``CRITICAL`` threshold.
        :type critical: float, optional

        :param critical_recovery: The monitor ``CRITICAL`` recovery threshold.
        :type critical_recovery: float, none_type, optional

        :param ok: The monitor ``OK`` threshold.
        :type ok: float, none_type, optional

        :param unknown: The monitor UNKNOWN threshold.
        :type unknown: float, none_type, optional

        :param warning: The monitor ``WARNING`` threshold.
        :type warning: float, none_type, optional

        :param warning_recovery: The monitor ``WARNING`` recovery threshold.
        :type warning_recovery: float, none_type, optional
        """
        if critical is not unset:
            kwargs["critical"] = critical
        if critical_recovery is not unset:
            kwargs["critical_recovery"] = critical_recovery
        if ok is not unset:
            kwargs["ok"] = ok
        if unknown is not unset:
            kwargs["unknown"] = unknown
        if warning is not unset:
            kwargs["warning"] = warning
        if warning_recovery is not unset:
            kwargs["warning_recovery"] = warning_recovery
        super().__init__(kwargs)
