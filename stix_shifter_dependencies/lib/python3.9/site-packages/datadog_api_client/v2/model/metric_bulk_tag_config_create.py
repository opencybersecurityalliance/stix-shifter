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
    from datadog_api_client.v2.model.metric_bulk_tag_config_create_attributes import MetricBulkTagConfigCreateAttributes
    from datadog_api_client.v2.model.metric_bulk_configure_tags_type import MetricBulkConfigureTagsType


class MetricBulkTagConfigCreate(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.metric_bulk_tag_config_create_attributes import (
            MetricBulkTagConfigCreateAttributes,
        )
        from datadog_api_client.v2.model.metric_bulk_configure_tags_type import MetricBulkConfigureTagsType

        return {
            "attributes": (MetricBulkTagConfigCreateAttributes,),
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
        attributes: Union[MetricBulkTagConfigCreateAttributes, UnsetType] = unset,
        **kwargs,
    ):
        """
        Request object to bulk configure tags for metrics matching the given prefix.

        :param attributes: Optional parameters for bulk creating metric tag configurations.
        :type attributes: MetricBulkTagConfigCreateAttributes, optional

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
