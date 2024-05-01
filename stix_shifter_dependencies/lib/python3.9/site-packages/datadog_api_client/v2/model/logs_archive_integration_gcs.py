# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
)


class LogsArchiveIntegrationGCS(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "client_email": (str,),
            "project_id": (str,),
        }

    attribute_map = {
        "client_email": "client_email",
        "project_id": "project_id",
    }

    def __init__(self_, client_email: str, project_id: str, **kwargs):
        """
        The GCS archive's integration destination.

        :param client_email: A client email.
        :type client_email: str

        :param project_id: A project ID.
        :type project_id: str
        """
        super().__init__(kwargs)

        self_.client_email = client_email
        self_.project_id = project_id
