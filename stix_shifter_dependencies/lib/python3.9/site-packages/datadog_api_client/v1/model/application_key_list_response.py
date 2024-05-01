# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import List, Union, TYPE_CHECKING

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    unset,
    UnsetType,
)


if TYPE_CHECKING:
    from datadog_api_client.v1.model.application_key import ApplicationKey


class ApplicationKeyListResponse(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.application_key import ApplicationKey

        return {
            "application_keys": ([ApplicationKey],),
        }

    attribute_map = {
        "application_keys": "application_keys",
    }

    def __init__(self_, application_keys: Union[List[ApplicationKey], UnsetType] = unset, **kwargs):
        """
        An application key response.

        :param application_keys: Array of application keys.
        :type application_keys: [ApplicationKey], optional
        """
        if application_keys is not unset:
            kwargs["application_keys"] = application_keys
        super().__init__(kwargs)
