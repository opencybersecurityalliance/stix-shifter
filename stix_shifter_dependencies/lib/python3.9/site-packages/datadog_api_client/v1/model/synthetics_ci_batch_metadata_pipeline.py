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


class SyntheticsCIBatchMetadataPipeline(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "url": (str,),
        }

    attribute_map = {
        "url": "url",
    }

    def __init__(self_, url: Union[str, UnsetType] = unset, **kwargs):
        """
        Description of the CI pipeline.

        :param url: URL of the pipeline.
        :type url: str, optional
        """
        if url is not unset:
            kwargs["url"] = url
        super().__init__(kwargs)
