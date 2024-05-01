# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
)


class FunnelStep(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "facet": (str,),
            "value": (str,),
        }

    attribute_map = {
        "facet": "facet",
        "value": "value",
    }

    def __init__(self_, facet: str, value: str, **kwargs):
        """
        The funnel step.

        :param facet: The facet of the step.
        :type facet: str

        :param value: The value of the step.
        :type value: str
        """
        super().__init__(kwargs)

        self_.facet = facet
        self_.value = value
