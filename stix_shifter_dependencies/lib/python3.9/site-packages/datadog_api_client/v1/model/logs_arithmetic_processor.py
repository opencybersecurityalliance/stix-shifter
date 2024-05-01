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
    from datadog_api_client.v1.model.logs_arithmetic_processor_type import LogsArithmeticProcessorType


class LogsArithmeticProcessor(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.logs_arithmetic_processor_type import LogsArithmeticProcessorType

        return {
            "expression": (str,),
            "is_enabled": (bool,),
            "is_replace_missing": (bool,),
            "name": (str,),
            "target": (str,),
            "type": (LogsArithmeticProcessorType,),
        }

    attribute_map = {
        "expression": "expression",
        "is_enabled": "is_enabled",
        "is_replace_missing": "is_replace_missing",
        "name": "name",
        "target": "target",
        "type": "type",
    }

    def __init__(
        self_,
        expression: str,
        target: str,
        type: LogsArithmeticProcessorType,
        is_enabled: Union[bool, UnsetType] = unset,
        is_replace_missing: Union[bool, UnsetType] = unset,
        name: Union[str, UnsetType] = unset,
        **kwargs,
    ):
        """
        Use the Arithmetic Processor to add a new attribute (without spaces or special characters
        in the new attribute name) to a log with the result of the provided formula.
        This enables you to remap different time attributes with different units into a single attribute,
        or to compute operations on attributes within the same log.

        The formula can use parentheses and the basic arithmetic operators ``-`` , ``+`` , ``*`` , ``/``.

        By default, the calculation is skipped if an attribute is missing.
        Select “Replace missing attribute by 0” to automatically populate
        missing attribute values with 0 to ensure that the calculation is done.
        An attribute is missing if it is not found in the log attributes,
        or if it cannot be converted to a number.

        *Notes* :

        * The operator ``-`` needs to be space split in the formula as it can also be contained in attribute names.
        * If the target attribute already exists, it is overwritten by the result of the formula.
        * Results are rounded up to the 9th decimal. For example, if the result of the formula is ``0.1234567891`` ,
          the actual value stored for the attribute is ``0.123456789``.
        * If you need to scale a unit of measure,
          see `Scale Filter <https://docs.datadoghq.com/logs/log_configuration/parsing/?tab=filter#matcher-and-filter>`_.

        :param expression: Arithmetic operation between one or more log attributes.
        :type expression: str

        :param is_enabled: Whether or not the processor is enabled.
        :type is_enabled: bool, optional

        :param is_replace_missing: If ``true`` , it replaces all missing attributes of expression by ``0`` , ``false``
            skip the operation if an attribute is missing.
        :type is_replace_missing: bool, optional

        :param name: Name of the processor.
        :type name: str, optional

        :param target: Name of the attribute that contains the result of the arithmetic operation.
        :type target: str

        :param type: Type of logs arithmetic processor.
        :type type: LogsArithmeticProcessorType
        """
        if is_enabled is not unset:
            kwargs["is_enabled"] = is_enabled
        if is_replace_missing is not unset:
            kwargs["is_replace_missing"] = is_replace_missing
        if name is not unset:
            kwargs["name"] = name
        super().__init__(kwargs)

        self_.expression = expression
        self_.target = target
        self_.type = type
