# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class FastlyAccountType(ModelSimple):
    """
    The JSON:API type for this API. Should always be `fastly-accounts`.

    :param value: If omitted defaults to "fastly-accounts". Must be one of ["fastly-accounts"].
    :type value: str
    """

    allowed_values = {
        "fastly-accounts",
    }
    FASTLY_ACCOUNTS: ClassVar["FastlyAccountType"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


FastlyAccountType.FASTLY_ACCOUNTS = FastlyAccountType("fastly-accounts")
