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
    from datadog_api_client.v1.model.target_format_type import TargetFormatType
    from datadog_api_client.v1.model.logs_attribute_remapper_type import LogsAttributeRemapperType


class LogsAttributeRemapper(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.target_format_type import TargetFormatType
        from datadog_api_client.v1.model.logs_attribute_remapper_type import LogsAttributeRemapperType

        return {
            "is_enabled": (bool,),
            "name": (str,),
            "override_on_conflict": (bool,),
            "preserve_source": (bool,),
            "source_type": (str,),
            "sources": ([str],),
            "target": (str,),
            "target_format": (TargetFormatType,),
            "target_type": (str,),
            "type": (LogsAttributeRemapperType,),
        }

    attribute_map = {
        "is_enabled": "is_enabled",
        "name": "name",
        "override_on_conflict": "override_on_conflict",
        "preserve_source": "preserve_source",
        "source_type": "source_type",
        "sources": "sources",
        "target": "target",
        "target_format": "target_format",
        "target_type": "target_type",
        "type": "type",
    }

    def __init__(
        self_,
        sources: List[str],
        target: str,
        type: LogsAttributeRemapperType,
        is_enabled: Union[bool, UnsetType] = unset,
        name: Union[str, UnsetType] = unset,
        override_on_conflict: Union[bool, UnsetType] = unset,
        preserve_source: Union[bool, UnsetType] = unset,
        source_type: Union[str, UnsetType] = unset,
        target_format: Union[TargetFormatType, UnsetType] = unset,
        target_type: Union[str, UnsetType] = unset,
        **kwargs,
    ):
        """
        The remapper processor remaps any source attribute(s) or tag to another target attribute or tag.
        Constraints on the tag/attribute name are explained in the `Tag Best Practice documentation <https://docs.datadoghq.com/logs/guide/log-parsing-best-practice>`_.
        Some additional constraints are applied as ``:`` or ``,`` are not allowed in the target tag/attribute name.

        :param is_enabled: Whether or not the processor is enabled.
        :type is_enabled: bool, optional

        :param name: Name of the processor.
        :type name: str, optional

        :param override_on_conflict: Override or not the target element if already set,
        :type override_on_conflict: bool, optional

        :param preserve_source: Remove or preserve the remapped source element.
        :type preserve_source: bool, optional

        :param source_type: Defines if the sources are from log ``attribute`` or ``tag``.
        :type source_type: str, optional

        :param sources: Array of source attributes.
        :type sources: [str]

        :param target: Final attribute or tag name to remap the sources to.
        :type target: str

        :param target_format: If the ``target_type`` of the remapper is ``attribute`` , try to cast the value to a new specific type.
            If the cast is not possible, the original type is kept. ``string`` , ``integer`` , or ``double`` are the possible types.
            If the ``target_type`` is ``tag`` , this parameter may not be specified.
        :type target_format: TargetFormatType, optional

        :param target_type: Defines if the final attribute or tag name is from log ``attribute`` or ``tag``.
        :type target_type: str, optional

        :param type: Type of logs attribute remapper.
        :type type: LogsAttributeRemapperType
        """
        if is_enabled is not unset:
            kwargs["is_enabled"] = is_enabled
        if name is not unset:
            kwargs["name"] = name
        if override_on_conflict is not unset:
            kwargs["override_on_conflict"] = override_on_conflict
        if preserve_source is not unset:
            kwargs["preserve_source"] = preserve_source
        if source_type is not unset:
            kwargs["source_type"] = source_type
        if target_format is not unset:
            kwargs["target_format"] = target_format
        if target_type is not unset:
            kwargs["target_type"] = target_type
        super().__init__(kwargs)

        self_.sources = sources
        self_.target = target
        self_.type = type
