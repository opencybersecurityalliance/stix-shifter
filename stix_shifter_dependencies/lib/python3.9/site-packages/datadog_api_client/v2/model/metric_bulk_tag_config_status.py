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
    from datadog_api_client.v2.model.metric_bulk_tag_config_status_attributes import MetricBulkTagConfigStatusAttributes
    from datadog_api_client.v2.model.metric_bulk_configure_tags_type import MetricBulkConfigureTagsType


class MetricBulkTagConfigStatus(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.metric_bulk_tag_config_status_attributes import (
            MetricBulkTagConfigStatusAttributes,
        )
        from datadog_api_client.v2.model.metric_bulk_configure_tags_type import MetricBulkConfigureTagsType

        return {
            "attributes": (MetricBulkTagConfigStatusAttributes,),
            "id": (str,),
            "type": (MetricBulkConfigureTagsType,),
        }

    attribute_map = {
        "attributes": "attributes",
        "id": "id",
        "type": "type",
    }

    def __init__(
        self_,
        id: str,
        type: MetricBulkConfigureTagsType,
        attributes: Union[MetricBulkTagConfigStatusAttributes, UnsetType] = unset,
        **kwargs,
    ):
        """
        The status of a request to bulk configure metric tags.
        It contains the fields from the original request for reference.

        :param attributes: Optional attributes for the status of a bulk tag configuration request.
        :type attributes: MetricBulkTagConfigStatusAttributes, optional

        :param id: A text prefix to match against metric names.
        :type id: str

        :param type: The metric bulk configure tags resource.
        :type type: MetricBulkConfigureTagsType
        """
        if attributes is not unset:
            kwargs["attributes"] = attributes
        super().__init__(kwargs)

        self_.id = id
        self_.type = type
