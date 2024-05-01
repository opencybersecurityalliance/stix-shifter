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
    from datadog_api_client.v1.model.logs_lookup_processor_type import LogsLookupProcessorType


class ReferenceTableLogsLookupProcessor(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.logs_lookup_processor_type import LogsLookupProcessorType

        return {
            "is_enabled": (bool,),
            "lookup_enrichment_table": (str,),
            "name": (str,),
            "source": (str,),
            "target": (str,),
            "type": (LogsLookupProcessorType,),
        }

    attribute_map = {
        "is_enabled": "is_enabled",
        "lookup_enrichment_table": "lookup_enrichment_table",
        "name": "name",
        "source": "source",
        "target": "target",
        "type": "type",
    }

    def __init__(
        self_,
        lookup_enrichment_table: str,
        source: str,
        target: str,
        type: LogsLookupProcessorType,
        is_enabled: Union[bool, UnsetType] = unset,
        name: Union[str, UnsetType] = unset,
        **kwargs,
    ):
        """
        **Note** : Reference Tables are in public beta.
        Use the Lookup Processor to define a mapping between a log attribute
        and a human readable value saved in a Reference Table.
        For example, you can use the Lookup Processor to map an internal service ID
        into a human readable service name. Alternatively, you could also use it to check
        if the MAC address that just attempted to connect to the production
        environment belongs to your list of stolen machines.

        :param is_enabled: Whether or not the processor is enabled.
        :type is_enabled: bool, optional

        :param lookup_enrichment_table: Name of the Reference Table for the source attribute and their associated target attribute values.
        :type lookup_enrichment_table: str

        :param name: Name of the processor.
        :type name: str, optional

        :param source: Source attribute used to perform the lookup.
        :type source: str

        :param target: Name of the attribute that contains the corresponding value in the mapping list.
        :type target: str

        :param type: Type of logs lookup processor.
        :type type: LogsLookupProcessorType
        """
        if is_enabled is not unset:
            kwargs["is_enabled"] = is_enabled
        if name is not unset:
            kwargs["name"] = name
        super().__init__(kwargs)

        self_.lookup_enrichment_table = lookup_enrichment_table
        self_.source = source
        self_.target = target
        self_.type = type
