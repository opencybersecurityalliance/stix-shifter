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


class AWSLogsLambda(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "arn": (str,),
        }

    attribute_map = {
        "arn": "arn",
    }

    def __init__(self_, arn: Union[str, UnsetType] = unset, **kwargs):
        """
        Description of the Lambdas.

        :param arn: Available ARN IDs.
        :type arn: str, optional
        """
        if arn is not unset:
            kwargs["arn"] = arn
        super().__init__(kwargs)
