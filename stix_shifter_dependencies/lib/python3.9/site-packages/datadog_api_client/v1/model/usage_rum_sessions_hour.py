# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Union

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    datetime,
    none_type,
    unset,
    UnsetType,
)


class UsageRumSessionsHour(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "hour": (datetime,),
            "org_name": (str,),
            "public_id": (str,),
            "replay_session_count": (int,),
            "session_count": (int, none_type),
            "session_count_android": (int, none_type),
            "session_count_flutter": (int, none_type),
            "session_count_ios": (int, none_type),
            "session_count_reactnative": (int, none_type),
        }

    attribute_map = {
        "hour": "hour",
        "org_name": "org_name",
        "public_id": "public_id",
        "replay_session_count": "replay_session_count",
        "session_count": "session_count",
        "session_count_android": "session_count_android",
        "session_count_flutter": "session_count_flutter",
        "session_count_ios": "session_count_ios",
        "session_count_reactnative": "session_count_reactnative",
    }

    def __init__(
        self_,
        hour: Union[datetime, UnsetType] = unset,
        org_name: Union[str, UnsetType] = unset,
        public_id: Union[str, UnsetType] = unset,
        replay_session_count: Union[int, UnsetType] = unset,
        session_count: Union[int, none_type, UnsetType] = unset,
        session_count_android: Union[int, none_type, UnsetType] = unset,
        session_count_flutter: Union[int, none_type, UnsetType] = unset,
        session_count_ios: Union[int, none_type, UnsetType] = unset,
        session_count_reactnative: Union[int, none_type, UnsetType] = unset,
        **kwargs,
    ):
        """
        Number of RUM Sessions recorded for each hour for a given organization.

        :param hour: The hour for the usage.
        :type hour: datetime, optional

        :param org_name: The organization name.
        :type org_name: str, optional

        :param public_id: The organization public ID.
        :type public_id: str, optional

        :param replay_session_count: Contains the number of RUM Replay Sessions (data available beginning November 1, 2021).
        :type replay_session_count: int, optional

        :param session_count: Contains the number of browser RUM Lite Sessions.
        :type session_count: int, none_type, optional

        :param session_count_android: Contains the number of mobile RUM Sessions on Android (data available beginning December 1, 2020).
        :type session_count_android: int, none_type, optional

        :param session_count_flutter: Contains the number of mobile RUM Sessions on Flutter (data available beginning March 1, 2023).
        :type session_count_flutter: int, none_type, optional

        :param session_count_ios: Contains the number of mobile RUM Sessions on iOS (data available beginning December 1, 2020).
        :type session_count_ios: int, none_type, optional

        :param session_count_reactnative: Contains the number of mobile RUM Sessions on React Native (data available beginning May 1, 2022).
        :type session_count_reactnative: int, none_type, optional
        """
        if hour is not unset:
            kwargs["hour"] = hour
        if org_name is not unset:
            kwargs["org_name"] = org_name
        if public_id is not unset:
            kwargs["public_id"] = public_id
        if replay_session_count is not unset:
            kwargs["replay_session_count"] = replay_session_count
        if session_count is not unset:
            kwargs["session_count"] = session_count
        if session_count_android is not unset:
            kwargs["session_count_android"] = session_count_android
        if session_count_flutter is not unset:
            kwargs["session_count_flutter"] = session_count_flutter
        if session_count_ios is not unset:
            kwargs["session_count_ios"] = session_count_ios
        if session_count_reactnative is not unset:
            kwargs["session_count_reactnative"] = session_count_reactnative
        super().__init__(kwargs)
