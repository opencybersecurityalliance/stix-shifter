# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import List, Union, TYPE_CHECKING

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    none_type,
    unset,
    UnsetType,
)


if TYPE_CHECKING:
    from datadog_api_client.v1.model.creator import Creator
    from datadog_api_client.v1.model.monitor_search_result_notification import MonitorSearchResultNotification
    from datadog_api_client.v1.model.monitor_overall_states import MonitorOverallStates
    from datadog_api_client.v1.model.monitor_type import MonitorType


class MonitorSearchResult(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.creator import Creator
        from datadog_api_client.v1.model.monitor_search_result_notification import MonitorSearchResultNotification
        from datadog_api_client.v1.model.monitor_overall_states import MonitorOverallStates
        from datadog_api_client.v1.model.monitor_type import MonitorType

        return {
            "classification": (str,),
            "creator": (Creator,),
            "id": (int,),
            "last_triggered_ts": (int, none_type),
            "metrics": ([str],),
            "name": (str,),
            "notifications": ([MonitorSearchResultNotification],),
            "org_id": (int,),
            "query": (str,),
            "scopes": ([str],),
            "status": (MonitorOverallStates,),
            "tags": ([str],),
            "type": (MonitorType,),
        }

    attribute_map = {
        "classification": "classification",
        "creator": "creator",
        "id": "id",
        "last_triggered_ts": "last_triggered_ts",
        "metrics": "metrics",
        "name": "name",
        "notifications": "notifications",
        "org_id": "org_id",
        "query": "query",
        "scopes": "scopes",
        "status": "status",
        "tags": "tags",
        "type": "type",
    }
    read_only_vars = {
        "classification",
        "creator",
        "id",
        "last_triggered_ts",
        "metrics",
        "name",
        "notifications",
        "org_id",
        "status",
        "tags",
    }

    def __init__(
        self_,
        classification: Union[str, UnsetType] = unset,
        creator: Union[Creator, UnsetType] = unset,
        id: Union[int, UnsetType] = unset,
        last_triggered_ts: Union[int, none_type, UnsetType] = unset,
        metrics: Union[List[str], UnsetType] = unset,
        name: Union[str, UnsetType] = unset,
        notifications: Union[List[MonitorSearchResultNotification], UnsetType] = unset,
        org_id: Union[int, UnsetType] = unset,
        query: Union[str, UnsetType] = unset,
        scopes: Union[List[str], UnsetType] = unset,
        status: Union[MonitorOverallStates, UnsetType] = unset,
        tags: Union[List[str], UnsetType] = unset,
        type: Union[MonitorType, UnsetType] = unset,
        **kwargs,
    ):
        """
        Holds search results.

        :param classification: Classification of the monitor.
        :type classification: str, optional

        :param creator: Object describing the creator of the shared element.
        :type creator: Creator, optional

        :param id: ID of the monitor.
        :type id: int, optional

        :param last_triggered_ts: Latest timestamp the monitor triggered.
        :type last_triggered_ts: int, none_type, optional

        :param metrics: Metrics used by the monitor.
        :type metrics: [str], optional

        :param name: The monitor name.
        :type name: str, optional

        :param notifications: The notification triggered by the monitor.
        :type notifications: [MonitorSearchResultNotification], optional

        :param org_id: The ID of the organization.
        :type org_id: int, optional

        :param query: The monitor query.
        :type query: str, optional

        :param scopes: The scope(s) to which the downtime applies, for example ``host:app2``.
            Provide multiple scopes as a comma-separated list, for example ``env:dev,env:prod``.
            The resulting downtime applies to sources that matches ALL provided scopes
            (that is ``env:dev AND env:prod`` ), NOT any of them.
        :type scopes: [str], optional

        :param status: The different states your monitor can be in.
        :type status: MonitorOverallStates, optional

        :param tags: Tags associated with the monitor.
        :type tags: [str], optional

        :param type: The type of the monitor. For more information about ``type`` , see the `monitor options <https://docs.datadoghq.com/monitors/guide/monitor_api_options/>`_ docs.
        :type type: MonitorType, optional
        """
        if classification is not unset:
            kwargs["classification"] = classification
        if creator is not unset:
            kwargs["creator"] = creator
        if id is not unset:
            kwargs["id"] = id
        if last_triggered_ts is not unset:
            kwargs["last_triggered_ts"] = last_triggered_ts
        if metrics is not unset:
            kwargs["metrics"] = metrics
        if name is not unset:
            kwargs["name"] = name
        if notifications is not unset:
            kwargs["notifications"] = notifications
        if org_id is not unset:
            kwargs["org_id"] = org_id
        if query is not unset:
            kwargs["query"] = query
        if scopes is not unset:
            kwargs["scopes"] = scopes
        if status is not unset:
            kwargs["status"] = status
        if tags is not unset:
            kwargs["tags"] = tags
        if type is not unset:
            kwargs["type"] = type
        super().__init__(kwargs)
