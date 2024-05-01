# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
)


class LogsArchiveIntegrationS3(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "account_id": (str,),
            "role_name": (str,),
        }

    attribute_map = {
        "account_id": "account_id",
        "role_name": "role_name",
    }

    def __init__(self_, account_id: str, role_name: str, **kwargs):
        """
        The S3 Archive's integration destination.

        :param account_id: The account ID for the integration.
        :type account_id: str

        :param role_name: The path of the integration.
        :type role_name: str
        """
        super().__init__(kwargs)

        self_.account_id = account_id
        self_.role_name = role_name
