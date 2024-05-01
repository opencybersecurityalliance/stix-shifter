# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Dict, Union, TYPE_CHECKING

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    unset,
    UnsetType,
)


if TYPE_CHECKING:
    from datadog_api_client.v1.model.monitor_state_group import MonitorStateGroup


class MonitorState(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.monitor_state_group import MonitorStateGroup

        return {
            "groups": ({str: (MonitorStateGroup,)},),
        }

    attribute_map = {
        "groups": "groups",
    }

    def __init__(self_, groups: Union[Dict[str, MonitorStateGroup], UnsetType] = unset, **kwargs):
        """
        Wrapper object with the different monitor states.

        :param groups: Dictionary where the keys are groups (comma separated lists of tags) and the values are
            the list of groups your monitor is broken down on.
        :type groups: {str: (MonitorStateGroup,)}, optional
        """
        if groups is not unset:
            kwargs["groups"] = groups
        super().__init__(kwargs)
