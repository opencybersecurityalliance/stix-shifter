# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Dict, List, Union, TYPE_CHECKING

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    datetime,
    none_type,
    unset,
    UnsetType,
)


if TYPE_CHECKING:
    from datadog_api_client.v2.model.incident_field_attributes import IncidentFieldAttributes
    from datadog_api_client.v2.model.incident_notification_handle import IncidentNotificationHandle
    from datadog_api_client.v2.model.incident_field_attributes_single_value import IncidentFieldAttributesSingleValue
    from datadog_api_client.v2.model.incident_field_attributes_multiple_value import (
        IncidentFieldAttributesMultipleValue,
    )


class IncidentUpdateAttributes(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.incident_field_attributes import IncidentFieldAttributes
        from datadog_api_client.v2.model.incident_notification_handle import IncidentNotificationHandle

        return {
            "customer_impact_end": (datetime, none_type),
            "customer_impact_scope": (str,),
            "customer_impact_start": (datetime, none_type),
            "customer_impacted": (bool,),
            "detected": (datetime, none_type),
            "fields": ({str: (IncidentFieldAttributes,)},),
            "notification_handles": ([IncidentNotificationHandle],),
            "title": (str,),
        }

    attribute_map = {
        "customer_impact_end": "customer_impact_end",
        "customer_impact_scope": "customer_impact_scope",
        "customer_impact_start": "customer_impact_start",
        "customer_impacted": "customer_impacted",
        "detected": "detected",
        "fields": "fields",
        "notification_handles": "notification_handles",
        "title": "title",
    }

    def __init__(
        self_,
        customer_impact_end: Union[datetime, none_type, UnsetType] = unset,
        customer_impact_scope: Union[str, UnsetType] = unset,
        customer_impact_start: Union[datetime, none_type, UnsetType] = unset,
        customer_impacted: Union[bool, UnsetType] = unset,
        detected: Union[datetime, none_type, UnsetType] = unset,
        fields: Union[
            Dict[
                str,
                Union[
                    IncidentFieldAttributes, IncidentFieldAttributesSingleValue, IncidentFieldAttributesMultipleValue
                ],
            ],
            UnsetType,
        ] = unset,
        notification_handles: Union[List[IncidentNotificationHandle], UnsetType] = unset,
        title: Union[str, UnsetType] = unset,
        **kwargs,
    ):
        """
        The incident's attributes for an update request.

        :param customer_impact_end: Timestamp when customers were no longer impacted by the incident.
        :type customer_impact_end: datetime, none_type, optional

        :param customer_impact_scope: A summary of the impact customers experienced during the incident.
        :type customer_impact_scope: str, optional

        :param customer_impact_start: Timestamp when customers began being impacted by the incident.
        :type customer_impact_start: datetime, none_type, optional

        :param customer_impacted: A flag indicating whether the incident caused customer impact.
        :type customer_impacted: bool, optional

        :param detected: Timestamp when the incident was detected.
        :type detected: datetime, none_type, optional

        :param fields: A condensed view of the user-defined fields for which to update selections.
        :type fields: {str: (IncidentFieldAttributes,)}, optional

        :param notification_handles: Notification handles that will be notified of the incident during update.
        :type notification_handles: [IncidentNotificationHandle], optional

        :param title: The title of the incident, which summarizes what happened.
        :type title: str, optional
        """
        if customer_impact_end is not unset:
            kwargs["customer_impact_end"] = customer_impact_end
        if customer_impact_scope is not unset:
            kwargs["customer_impact_scope"] = customer_impact_scope
        if customer_impact_start is not unset:
            kwargs["customer_impact_start"] = customer_impact_start
        if customer_impacted is not unset:
            kwargs["customer_impacted"] = customer_impacted
        if detected is not unset:
            kwargs["detected"] = detected
        if fields is not unset:
            kwargs["fields"] = fields
        if notification_handles is not unset:
            kwargs["notification_handles"] = notification_handles
        if title is not unset:
            kwargs["title"] = title
        super().__init__(kwargs)
