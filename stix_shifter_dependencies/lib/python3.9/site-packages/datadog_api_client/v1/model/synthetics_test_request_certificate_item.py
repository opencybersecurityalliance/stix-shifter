# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Union

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    unset,
    UnsetType,
)


class SyntheticsTestRequestCertificateItem(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "content": (str,),
            "filename": (str,),
            "updated_at": (str,),
        }

    attribute_map = {
        "content": "content",
        "filename": "filename",
        "updated_at": "updatedAt",
    }

    def __init__(
        self_,
        content: Union[str, UnsetType] = unset,
        filename: Union[str, UnsetType] = unset,
        updated_at: Union[str, UnsetType] = unset,
        **kwargs,
    ):
        """
        Define a request certificate.

        :param content: Content of the certificate or key.
        :type content: str, optional

        :param filename: File name for the certificate or key.
        :type filename: str, optional

        :param updated_at: Date of update of the certificate or key, ISO format.
        :type updated_at: str, optional
        """
        if content is not unset:
            kwargs["content"] = content
        if filename is not unset:
            kwargs["filename"] = filename
        if updated_at is not unset:
            kwargs["updated_at"] = updated_at
        super().__init__(kwargs)
