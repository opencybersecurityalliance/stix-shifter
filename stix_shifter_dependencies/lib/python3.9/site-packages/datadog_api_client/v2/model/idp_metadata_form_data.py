# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Union

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    file_type,
    unset,
    UnsetType,
)


class IdPMetadataFormData(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "idp_file": (file_type,),
        }

    attribute_map = {
        "idp_file": "idp_file",
    }

    def __init__(self_, idp_file: Union[file_type, UnsetType] = unset, **kwargs):
        """
        The form data submitted to upload IdP metadata

        :param idp_file: The IdP metadata XML file
        :type idp_file: file_type, optional
        """
        if idp_file is not unset:
            kwargs["idp_file"] = idp_file
        super().__init__(kwargs)
