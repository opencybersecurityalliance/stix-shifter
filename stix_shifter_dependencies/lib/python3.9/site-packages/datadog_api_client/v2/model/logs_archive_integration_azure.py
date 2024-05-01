# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
)


class LogsArchiveIntegrationAzure(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "client_id": (str,),
            "tenant_id": (str,),
        }

    attribute_map = {
        "client_id": "client_id",
        "tenant_id": "tenant_id",
    }

    def __init__(self_, client_id: str, tenant_id: str, **kwargs):
        """
        The Azure archive's integration destination.

        :param client_id: A client ID.
        :type client_id: str

        :param tenant_id: A tenant ID.
        :type tenant_id: str
        """
        super().__init__(kwargs)

        self_.client_id = client_id
        self_.tenant_id = tenant_id
