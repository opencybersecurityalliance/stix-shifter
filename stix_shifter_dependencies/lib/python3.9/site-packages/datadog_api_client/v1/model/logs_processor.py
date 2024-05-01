# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelComposed,
    cached_property,
)


class LogsProcessor(ModelComposed):
    def __init__(self, **kwargs):
        """
        Definition of a logs processor.

        :param grok: Set of rules for the grok parser.
        :type grok: LogsGrokParserRules

        :param is_enabled: Whether or not the processor is enabled.
        :type is_enabled: bool, optional

        :param name: Name of the processor.
        :type name: str, optional

        :param samples: List of sample logs to test this grok parser.
        :type samples: [str], optional

        :param source: Name of the log attribute to parse.
        :type source: str

        :param type: Type of logs grok parser.
        :type type: LogsGrokParserType

        :param sources: Array of source attributes.
        :type sources: [str]

        :param override_on_conflict: Override or not the target element if already set,
        :type override_on_conflict: bool, optional

        :param preserve_source: Remove or preserve the remapped source element.
        :type preserve_source: bool, optional

        :param source_type: Defines if the sources are from log `attribute` or `tag`.
        :type source_type: str, optional

        :param target: Final attribute or tag name to remap the sources to.
        :type target: str

        :param target_format: If the `target_type` of the remapper is `attribute`, try to cast the value to a new specific type.
            If the cast is not possible, the original type is kept. `string`, `integer`, or `double` are the possible types.
            If the `target_type` is `tag`, this parameter may not be specified.
        :type target_format: TargetFormatType, optional

        :param target_type: Defines if the final attribute or tag name is from log `attribute` or `tag`.
        :type target_type: str, optional

        :param normalize_ending_slashes: Normalize the ending slashes or not.
        :type normalize_ending_slashes: bool, none_type, optional

        :param is_encoded: Define if the source attribute is URL encoded or not.
        :type is_encoded: bool, optional

        :param categories: Array of filters to match or not a log and their
            corresponding `name` to assign a custom value to the log.
        :type categories: [LogsCategoryProcessorCategory]

        :param expression: Arithmetic operation between one or more log attributes.
        :type expression: str

        :param is_replace_missing: If `true`, it replaces all missing attributes of expression by `0`, `false`
            skip the operation if an attribute is missing.
        :type is_replace_missing: bool, optional

        :param template: A formula with one or more attributes and raw text.
        :type template: str

        :param filter: Filter for logs.
        :type filter: LogsFilter, optional

        :param processors: Ordered list of processors in this pipeline.
        :type processors: [LogsProcessor], optional

        :param default_lookup: Value to set the target attribute if the source value is not found in the list.
        :type default_lookup: str, optional

        :param lookup_table: Mapping table of values for the source attribute and their associated target attribute values,
            formatted as `["source_key1,target_value1", "source_key2,target_value2"]`
        :type lookup_table: [str]

        :param lookup_enrichment_table: Name of the Reference Table for the source attribute and their associated target attribute values.
        :type lookup_enrichment_table: str
        """
        super().__init__(kwargs)

    @cached_property
    def _composed_schemas(_):
        # we need this here to make our import statements work
        # we must store _composed_schemas in here so the code is only run
        # when we invoke this method. If we kept this at the class
        # level we would get an error because the class level
        # code would be run when this module is imported, and these composed
        # classes don't exist yet because their module has not finished
        # loading
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

        return {
            "oneOf": [
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
            ],
        }
