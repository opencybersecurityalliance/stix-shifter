# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Union, TYPE_CHECKING

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    none_type,
    unset,
    UnsetType,
)


if TYPE_CHECKING:
    from datadog_api_client.v1.model.notebook_metadata_type import NotebookMetadataType


class NotebookMetadata(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.notebook_metadata_type import NotebookMetadataType

        return {
            "is_template": (bool,),
            "take_snapshots": (bool,),
            "type": (NotebookMetadataType,),
        }

    attribute_map = {
        "is_template": "is_template",
        "take_snapshots": "take_snapshots",
        "type": "type",
    }

    def __init__(
        self_,
        is_template: Union[bool, UnsetType] = unset,
        take_snapshots: Union[bool, UnsetType] = unset,
        type: Union[NotebookMetadataType, none_type, UnsetType] = unset,
        **kwargs,
    ):
        """
        Metadata associated with the notebook.

        :param is_template: Whether or not the notebook is a template.
        :type is_template: bool, optional

        :param take_snapshots: Whether or not the notebook takes snapshot image backups of the notebook's fixed-time graphs.
        :type take_snapshots: bool, optional

        :param type: Metadata type of the notebook.
        :type type: NotebookMetadataType, none_type, optional
        """
        if is_template is not unset:
            kwargs["is_template"] = is_template
        if take_snapshots is not unset:
            kwargs["take_snapshots"] = take_snapshots
        if type is not unset:
            kwargs["type"] = type
        super().__init__(kwargs)
