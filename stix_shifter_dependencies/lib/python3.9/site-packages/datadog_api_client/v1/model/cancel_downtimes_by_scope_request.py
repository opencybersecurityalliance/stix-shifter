# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
)


class CancelDowntimesByScopeRequest(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "scope": (str,),
        }

    attribute_map = {
        "scope": "scope",
    }

    def __init__(self_, scope: str, **kwargs):
        """
        Cancel downtimes according to scope.

        :param scope: The scope(s) to which the downtime applies and must be in ``key:value`` format. For example, ``host:app2``.
            Provide multiple scopes as a comma-separated list like ``env:dev,env:prod``.
            The resulting downtime applies to sources that matches ALL provided scopes ( ``env:dev`` **AND** ``env:prod`` ).
        :type scope: str
        """
        super().__init__(kwargs)

        self_.scope = scope
