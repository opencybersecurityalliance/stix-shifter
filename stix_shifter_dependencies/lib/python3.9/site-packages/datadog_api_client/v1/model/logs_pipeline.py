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
    from datadog_api_client.v1.model.logs_pipeline_processor import LogsPipelineProcessor
    from datadog_api_client.v1.model.logs_geo_ip_parser import LogsGeoIPParser
    from datadog_api_client.v1.model.logs_lookup_processor import LogsLookupProcessor
    from datadog_api_client.v1.model.reference_table_logs_lookup_processor import ReferenceTableLogsLookupProcessor
    from datadog_api_client.v1.model.logs_trace_remapper import LogsTraceRemapper


class LogsPipeline(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.logs_filter import LogsFilter
        from datadog_api_client.v1.model.logs_processor import LogsProcessor

        return {
            "filter": (LogsFilter,),
            "id": (str,),
            "is_enabled": (bool,),
            "is_read_only": (bool,),
            "name": (str,),
            "processors": ([LogsProcessor],),
            "type": (str,),
        }

    attribute_map = {
        "filter": "filter",
        "id": "id",
        "is_enabled": "is_enabled",
        "is_read_only": "is_read_only",
        "name": "name",
        "processors": "processors",
        "type": "type",
    }
    read_only_vars = {
        "id",
        "is_read_only",
        "type",
    }

    def __init__(
        self_,
        name: str,
        filter: Union[LogsFilter, UnsetType] = unset,
        id: Union[str, UnsetType] = unset,
        is_enabled: Union[bool, UnsetType] = unset,
        is_read_only: Union[bool, UnsetType] = unset,
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
        type: Union[str, UnsetType] = unset,
        **kwargs,
    ):
        """
        Pipelines and processors operate on incoming logs,
        parsing and transforming them into structured attributes for easier querying.

        **Note** : These endpoints are only available for admin users.
        Make sure to use an application key created by an admin.

        :param filter: Filter for logs.
        :type filter: LogsFilter, optional

        :param id: ID of the pipeline.
        :type id: str, optional

        :param is_enabled: Whether or not the pipeline is enabled.
        :type is_enabled: bool, optional

        :param is_read_only: Whether or not the pipeline can be edited.
        :type is_read_only: bool, optional

        :param name: Name of the pipeline.
        :type name: str

        :param processors: Ordered list of processors in this pipeline.
        :type processors: [LogsProcessor], optional

        :param type: Type of pipeline.
        :type type: str, optional
        """
        if filter is not unset:
            kwargs["filter"] = filter
        if id is not unset:
            kwargs["id"] = id
        if is_enabled is not unset:
            kwargs["is_enabled"] = is_enabled
        if is_read_only is not unset:
            kwargs["is_read_only"] = is_read_only
        if processors is not unset:
            kwargs["processors"] = processors
        if type is not unset:
            kwargs["type"] = type
        super().__init__(kwargs)

        self_.name = name
