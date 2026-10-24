from stix_shifter_utils.modules.base.stix_translation.base_query_translator import BaseQueryTranslator
import logging
import re
from os import path
import json
from . import query_constructor
from stix_shifter_utils.utils.file_helper import read_json
from datetime import datetime

logger = logging.getLogger(__name__)


class QueryTranslator(BaseQueryTranslator):

    def __init__(self, options, dialect, basepath, custom_mapping=None):
        super().__init__(options, dialect, basepath)
        self.supported_fields = {
            'hostname': r"hostname = '([^']+)'",
            'sourcemacaddress': r"sourcemacaddress = '([^']+)'",
            'resourcename': r"resourcename = '([^']+)'",
            'resourcetype': r"resourcetype = '([^']+)'",
            'destinationmacaddress': r"destinationmacaddress = '([^']+)'",
            'destinationport': r"destinationport = '(\d+)'",
            'categoryseverity': r"categoryseverity = '([^']+)'",
            'categoryid': r"categoryid = '([^']+)'",
            'resourcegroupid': r"resourcegroupid = '([^']+)'",
            'sourceport': r"sourceport = '(\d+)'",
            'devicehostname': r"devicehostname = '([^']+)'",
            'rg_vendor': r"rg_vendor = '([^']+)'",
            'rg_functionality': r"rg_functionality = '([^']+)'",
            'tenantname': r"tenantname = '([^']+)'",
            'tenantid': r"tenantid = '([^']+)'"
        }
        if custom_mapping:
            self.supported_fields.update(custom_mapping)

    def _extract_field_values(self, query_string, field_pattern):
        match = re.search(field_pattern, query_string)
        return match.group(1) if match else None

    def _get_field_value(self, query_string, field):
        if field in self.supported_fields:
            return self._extract_field_values(query_string, self.supported_fields[field])
        return None

    def transform_antlr(self, data, antlr_parsing_object):
        logger.info("Converting STIX2 Pattern to Securonix Query")

        query_string = query_constructor.translate_pattern(
            antlr_parsing_object, self, self.options)

        # Extract values for all supported fields
        field_values = {}
        for field in self.supported_fields:
            value = self._get_field_value(query_string, field)
            if value:
                field_values[field] = value

        # Add extracted values to query string
        for field, value in field_values.items():
            query_string = f"{query_string}&{field}={value}"

        # Handle timestamps
        timestamp_pattern = r"START t'([^']+)' STOP t'([^']+)'"
        match = re.search(timestamp_pattern, data)
        if match:
            start_time = datetime.strptime(match.group(1), '%Y-%m-%dT%H:%M:%S.%fZ')
            end_time = datetime.strptime(match.group(2), '%Y-%m-%dT%H:%M:%S.%fZ')
            formatted_start = start_time.strftime('%m/%d/%Y %H:%M:%S')
            formatted_end = end_time.strftime('%m/%d/%Y %H:%M:%S')
            query_string = f"{query_string}&eventtime_from={formatted_start}&eventtime_to={formatted_end}"

        return query_string
