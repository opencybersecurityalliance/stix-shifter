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
    from datadog_api_client.v1.model.logs_filter import LogsFilter
    from datadog_api_client.v1.model.logs_processor import LogsProcessor
    from datadog_api_client.v1.model.logs_pipeline_processor_type import LogsPipelineProcessorType
    from datadog_api_client.v1.model.logs_grok_parser import LogsGrokParser
    from datadog_api_client.v1.model.logs_date_remapper import LogsDateRemapper
    from datadog_api_client.v1.model.logs_status_remapper import LogsStatusRemapper
    from datadog_api_client.v1.model.logs_service_remapper import LogsServiceRemapper
    from datadog_api_client.v1.model.logs_message_remapper import LogsMessageRemapper
    from datadog_api_client.v1.model.logs_attribute_remapper import LogsAttributeRemapper
    from datadog_api_client.v1.model.logs_url_parser import LogsURLParser
    from datadog_api_client.v1.model.logs_user_agent_parser import LogsUserAgentParser
    from datadog_api_client.v1.model.logs_category_processor import LogsCategoryProcessor
    from datadog_api_client.v1.model.logs_arithmetic_processor import LogsArithmeticProcessor
    from datadog_api_client.v1.model.logs_string_builder_processor import LogsStringBuilderProcessor
    from datadog_api_client.v1.model.logs_geo_ip_parser import LogsGeoIPParser
    from datadog_api_client.v1.model.logs_lookup_processor import LogsLookupProcessor
    from datadog_api_client.v1.model.reference_table_logs_lookup_processor import ReferenceTableLogsLookupProcessor
    from datadog_api_client.v1.model.logs_trace_remapper import LogsTraceRemapper


class LogsPipelineProcessor(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.logs_filter import LogsFilter
        from datadog_api_client.v1.model.logs_processor import LogsProcessor
        from datadog_api_client.v1.model.logs_pipeline_processor_type import LogsPipelineProcessorType

        return {
            "filter": (LogsFilter,),
            "is_enabled": (bool,),
            "name": (str,),
            "processors": ([LogsProcessor],),
            "type": (LogsPipelineProcessorType,),
        }

    attribute_map = {
        "filter": "filter",
        "is_enabled": "is_enabled",
        "name": "name",
        "processors": "processors",
        "type": "type",
    }

    def __init__(
        self_,
        type: LogsPipelineProcessorType,
        filter: Union[LogsFilter, UnsetType] = unset,
        is_enabled: Union[bool, UnsetType] = unset,
        name: Union[str, UnsetType] = unset,
        processors: Union[
            List[
                Union[
                    LogsProcessor,
                    LogsGrokParser,
                    LogsDateRemapper,
                    LogsStatusRemapper,
                    LogsServiceRemapper,
                    LogsMessageRemapper,
                    LogsAttributeRemapper,
                    LogsURLParser,
                    LogsUserAgentParser,
                    LogsCategoryProcessor,
                    LogsArithmeticProcessor,
                    LogsStringBuilderProcessor,
                    LogsPipelineProcessor,
                    LogsGeoIPParser,
                    LogsLookupProcessor,
                    ReferenceTableLogsLookupProcessor,
                    LogsTraceRemapper,
                ]
            ],
            UnsetType,
        ] = unset,
        **kwargs,
    ):
        """
        Nested Pipelines are pipelines within a pipeline. Use Nested Pipelines to split the processing into two steps.
        For example, first use a high-level filtering such as team and then a second level of filtering based on the
        integration, service, or any other tag or attribute.

        A pipeline can contain Nested Pipelines and Processors whereas a Nested Pipeline can only contain Processors.

        :param filter: Filter for logs.
        :type filter: LogsFilter, optional

        :param is_enabled: Whether or not the processor is enabled.
        :type is_enabled: bool, optional

        :param name: Name of the processor.
        :type name: str, optional

        :param processors: Ordered list of processors in this pipeline.
        :type processors: [LogsProcessor], optional

        :param type: Type of logs pipeline processor.
        :type type: LogsPipelineProcessorType
        """
        if filter is not unset:
            kwargs["filter"] = filter
        if is_enabled is not unset:
            kwargs["is_enabled"] = is_enabled
        if name is not unset:
            kwargs["name"] = name
        if processors is not unset:
            kwargs["processors"] = processors
        super().__init__(kwargs)

        self_.type = type
