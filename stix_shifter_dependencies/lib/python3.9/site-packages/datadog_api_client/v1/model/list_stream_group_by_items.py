# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
)


class ListStreamGroupByItems(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "facet": (str,),
        }

    attribute_map = {
        "facet": "facet",
    }

    def __init__(self_, facet: str, **kwargs):
        """
        List of facets on which to group.

        :param facet: Facet name.
        :type facet: str
        """
        super().__init__(kwargs)

        self_.facet = facet
