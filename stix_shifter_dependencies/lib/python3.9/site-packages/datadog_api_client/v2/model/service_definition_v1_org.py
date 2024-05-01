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


class ServiceDefinitionV1Org(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "application": (str,),
            "team": (str,),
        }

    attribute_map = {
        "application": "application",
        "team": "team",
    }

    def __init__(self_, application: Union[str, UnsetType] = unset, team: Union[str, UnsetType] = unset, **kwargs):
        """
        Org related information about the service.

        :param application: App feature this service supports.
        :type application: str, optional

        :param team: Team that owns the service.
        :type team: str, optional
        """
        if application is not unset:
            kwargs["application"] = application
        if team is not unset:
            kwargs["team"] = team
        super().__init__(kwargs)
