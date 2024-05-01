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
    from datadog_api_client.v1.model.signal_archive_reason import SignalArchiveReason
    from datadog_api_client.v1.model.signal_triage_state import SignalTriageState


class SignalStateUpdateRequest(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.signal_archive_reason import SignalArchiveReason
        from datadog_api_client.v1.model.signal_triage_state import SignalTriageState

        return {
            "archive_comment": (str,),
            "archive_reason": (SignalArchiveReason,),
            "state": (SignalTriageState,),
            "version": (int,),
        }

    attribute_map = {
        "archive_comment": "archiveComment",
        "archive_reason": "archiveReason",
        "state": "state",
        "version": "version",
    }

    def __init__(
        self_,
        state: SignalTriageState,
        archive_comment: Union[str, UnsetType] = unset,
        archive_reason: Union[SignalArchiveReason, UnsetType] = unset,
        version: Union[int, UnsetType] = unset,
        **kwargs,
    ):
        """
        Attributes describing the change of state for a given state.

        :param archive_comment: Optional comment to explain why a signal is being archived.
        :type archive_comment: str, optional

        :param archive_reason: Reason why a signal has been archived.
        :type archive_reason: SignalArchiveReason, optional

        :param state: The new triage state of the signal.
        :type state: SignalTriageState

        :param version: Version of the updated signal. If server side version is higher, update will be rejected.
        :type version: int, optional
        """
        if archive_comment is not unset:
            kwargs["archive_comment"] = archive_comment
        if archive_reason is not unset:
            kwargs["archive_reason"] = archive_reason
        if version is not unset:
            kwargs["version"] = version
        super().__init__(kwargs)

        self_.state = state
