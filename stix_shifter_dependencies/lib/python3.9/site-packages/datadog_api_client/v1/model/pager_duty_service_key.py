# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
)


class PagerDutyServiceKey(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "service_key": (str,),
        }

    attribute_map = {
        "service_key": "service_key",
    }

    def __init__(self_, service_key: str, **kwargs):
        """
        PagerDuty service object key.

        :param service_key: Your service key in PagerDuty.
        :type service_key: str
        """
        super().__init__(kwargs)

        self_.service_key = service_key
