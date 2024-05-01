# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import List

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
)


class AWSLogsServicesRequest(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "account_id": (str,),
            "services": ([str],),
        }

    attribute_map = {
        "account_id": "account_id",
        "services": "services",
    }

    def __init__(self_, account_id: str, services: List[str], **kwargs):
        """
        A list of current AWS services for which Datadog offers automatic log collection.

        :param account_id: Your AWS Account ID without dashes.
        :type account_id: str

        :param services: Array of services IDs set to enable automatic log collection. Discover the list of available services with the get list of AWS log ready services API endpoint.
        :type services: [str]
        """
        super().__init__(kwargs)

        self_.account_id = account_id
        self_.services = services
