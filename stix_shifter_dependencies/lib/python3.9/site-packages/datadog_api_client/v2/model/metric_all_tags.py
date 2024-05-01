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
    from datadog_api_client.v2.model.metric_all_tags_attributes import MetricAllTagsAttributes
    from datadog_api_client.v2.model.metric_type import MetricType


class MetricAllTags(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.metric_all_tags_attributes import MetricAllTagsAttributes
        from datadog_api_client.v2.model.metric_type import MetricType

        return {
            "attributes": (MetricAllTagsAttributes,),
            "id": (str,),
            "type": (MetricType,),
        }

    attribute_map = {
        "attributes": "attributes",
        "id": "id",
        "type": "type",
    }

    def __init__(
        self_,
        attributes: Union[MetricAllTagsAttributes, UnsetType] = unset,
        id: Union[str, UnsetType] = unset,
        type: Union[MetricType, UnsetType] = unset,
        **kwargs,
    ):
        """
        Object for a single metric's indexed tags.

        :param attributes: Object containing the definition of a metric's tags.
        :type attributes: MetricAllTagsAttributes, optional

        :param id: The metric name for this resource.
        :type id: str, optional

        :param type: The metric resource type.
        :type type: MetricType, optional
        """
        if attributes is not unset:
            kwargs["attributes"] = attributes
        if id is not unset:
            kwargs["id"] = id
        if type is not unset:
            kwargs["type"] = type
        super().__init__(kwargs)
