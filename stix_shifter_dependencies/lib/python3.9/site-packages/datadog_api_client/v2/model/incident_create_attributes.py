# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Dict, List, Union, TYPE_CHECKING

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    unset,
    UnsetType,
)


if TYPE_CHECKING:
    from datadog_api_client.v2.model.incident_field_attributes import IncidentFieldAttributes
    from datadog_api_client.v2.model.incident_timeline_cell_create_attributes import (
        IncidentTimelineCellCreateAttributes,
    )
    from datadog_api_client.v2.model.incident_notification_handle import IncidentNotificationHandle
    from datadog_api_client.v2.model.incident_field_attributes_single_value import IncidentFieldAttributesSingleValue
    from datadog_api_client.v2.model.incident_field_attributes_multiple_value import (
        IncidentFieldAttributesMultipleValue,
    )
    from datadog_api_client.v2.model.incident_timeline_cell_markdown_create_attributes import (
        IncidentTimelineCellMarkdownCreateAttributes,
    )


class IncidentCreateAttributes(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.incident_field_attributes import IncidentFieldAttributes
        from datadog_api_client.v2.model.incident_timeline_cell_create_attributes import (
            IncidentTimelineCellCreateAttributes,
        )
        from datadog_api_client.v2.model.incident_notification_handle import IncidentNotificationHandle

        return {
            "customer_impacted": (bool,),
            "fields": ({str: (IncidentFieldAttributes,)},),
            "initial_cells": ([IncidentTimelineCellCreateAttributes],),
            "notification_handles": ([IncidentNotificationHandle],),
            "title": (str,),
        }

    attribute_map = {
        "customer_impacted": "customer_impacted",
        "fields": "fields",
        "initial_cells": "initial_cells",
        "notification_handles": "notification_handles",
        "title": "title",
    }

    def __init__(
        self_,
        customer_impacted: bool,
        title: str,
        fields: Union[
            Dict[
                str,
                Union[
                    IncidentFieldAttributes, IncidentFieldAttributesSingleValue, IncidentFieldAttributesMultipleValue
                ],
            ],
            UnsetType,
        ] = unset,
        initial_cells: Union[
            List[Union[IncidentTimelineCellCreateAttributes, IncidentTimelineCellMarkdownCreateAttributes]], UnsetType
        ] = unset,
        notification_handles: Union[List[IncidentNotificationHandle], UnsetType] = unset,
        **kwargs,
    ):
        """
        The incident's attributes for a create request.

        :param customer_impacted: A flag indicating whether the incident caused customer impact.
        :type customer_impacted: bool

        :param fields: A condensed view of the user-defined fields for which to create initial selections.
        :type fields: {str: (IncidentFieldAttributes,)}, optional

        :param initial_cells: An array of initial timeline cells to be placed at the beginning of the incident timeline.
        :type initial_cells: [IncidentTimelineCellCreateAttributes], optional

        :param notification_handles: Notification handles that will be notified of the incident at creation.
        :type notification_handles: [IncidentNotificationHandle], optional

        :param title: The title of the incident, which summarizes what happened.
        :type title: str
        """
        if fields is not unset:
            kwargs["fields"] = fields
        if initial_cells is not unset:
            kwargs["initial_cells"] = initial_cells
        if notification_handles is not unset:
            kwargs["notification_handles"] = notification_handles
        super().__init__(kwargs)

        self_.customer_impacted = customer_impacted
        self_.title = title
