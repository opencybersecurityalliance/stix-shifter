# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    file_type,
)


class IdpFormData(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "idp_file": (file_type,),
        }

    attribute_map = {
        "idp_file": "idp_file",
    }

    def __init__(self_, idp_file: file_type, **kwargs):
        """
        Object describing the IdP configuration.

        :param idp_file: The path to the XML metadata file you wish to upload.
        :type idp_file: file_type
        """
        super().__init__(kwargs)

        self_.idp_file = idp_file
