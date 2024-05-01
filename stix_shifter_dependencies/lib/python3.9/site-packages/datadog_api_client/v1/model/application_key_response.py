# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Union, TYPE_CHECKING

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    unset,
    UnsetType,
)


if TYPE_CHECKING:
    from datadog_api_client.v1.model.application_key import ApplicationKey


class ApplicationKeyResponse(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.application_key import ApplicationKey

        return {
            "application_key": (ApplicationKey,),
        }

    attribute_map = {
        "application_key": "application_key",
    }

    def __init__(self_, application_key: Union[ApplicationKey, UnsetType] = unset, **kwargs):
        """
        An application key response.

        :param application_key: An application key with its associated metadata.
        :type application_key: ApplicationKey, optional
        """
        if application_key is not unset:
            kwargs["application_key"] = application_key
        super().__init__(kwargs)
