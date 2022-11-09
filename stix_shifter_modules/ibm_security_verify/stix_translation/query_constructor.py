import json
import logging
import re
from datetime import datetime, timedelta
from typing import Union

from stix_shifter_utils.stix_translation.src.json_to_stix import observable
from stix_shifter_utils.stix_translation.src.patterns.pattern_objects import (
    CombinedComparisonExpression, CombinedObservationExpression,
    ComparisonComparators, ComparisonExpression, ComparisonExpressionOperators,
    ObservationExpression, ObservationOperators, Pattern)
from stix_shifter_utils.stix_translation.src.utils.transformers import \
    TimestampToMilliseconds

# Source and destination reference mapping for ip and mac addresses.
# Change the keys to match the data source fields. The value array indicates the possible data type that can come into from field.
REFERENCE_DATA_TYPES = {"ipaddr": ["ipv4", "ipv4_cidr", "ipv6", "ipv6_cidr"],
                        "proxy_ip": ["ipv4", "ipv4_cidr"],
                        }
REFERENCE_FILTER_TYPE = ["user-account",
                         "ipv4-addr", "domain-name", "x-oca-event"]
REFERENCE_EXCLUDE_FILTER_TYPE = ["category"]
logger = logging.getLogger(__name__)


class QueryStringPatternTranslator:
    QUERIES = []
 
    def __init__(self, pattern: Pattern, data_model_mapper):
        self.dmm = data_model_mapper
        self.comparator_lookup = self.dmm.map_comparator() 
        self.pattern = pattern
        self.translated = self.parse_expression(pattern)

    @staticmethod
    def _escape_value(value, comparator=None) -> str:
        if isinstance(value, str):
            return '{}'.format(value.replace("\'", "'").replace('\\', '\\\\').replace('(', '\\(').replace(')', '\\)').replace("$", "\"").replace('&', '%26')
                               .replace('""', '"'))
        else:
            return value

    @staticmethod
    def _convert_list_string_in_condition(value)->str:
        if isinstance(value, list):
            contcated_string = ''.join(
                f'"{str}",'.format(str) for str in value)
            contcated_string = contcated_string[1:-2]
            return contcated_string

    @staticmethod
    def _negate_comparison(comparison_string):
        return "NOT ({})".format(comparison_string)

    @staticmethod
    def _check_value_type(value):
        value = str(value)
        for key, pattern in observable.REGEX.items():
            if key != 'date' and bool(re.search(pattern, value)):
                return key
        return None

    # TODO remove self reference from static methods
    @staticmethod
    def _parse_reference(self, stix_field, value_type, mapped_field, value, comparator):
        if value_type not in REFERENCE_DATA_TYPES["{}".format(mapped_field)]:
            return None
        else:
            return "{mapped_field}{comparator}{value}".format(
                mapped_field=mapped_field, comparator=comparator, value=value)

    @staticmethod
    def _parse_mapped_fields(self, expression, value, comparator, stix_field, mapped_fields_array, stix_object):
        comparison_string = ""
        is_reference_value = self._is_reference_value(stix_field)
        is_object_filter_typeValue = self._is_object_filterType(
            stix_object, stix_field)
        # Need to use expression.value to match against regex since the passed-in value has already been formated.
        value_type = self._check_value_type(
            expression.value) if is_reference_value else None
        mapped_fields_count = 1 if is_reference_value else len(
            mapped_fields_array)

        for mapped_field in mapped_fields_array:
            if is_reference_value:
                parsed_reference = self._parse_reference(
                    self, stix_field, value_type, mapped_field, value, comparator)
                if not parsed_reference:
                    continue
                comparison_string += parsed_reference
            elif is_object_filter_typeValue:
                comparison_string += 'filter_key={mapped_field}&filter_value="{value}"'.format(
                    mapped_field=mapped_field, comparator=comparator, value=value)
            else:
                comparison_string += '{mapped_field}{comparator}"{value}"'.format(
                    mapped_field=mapped_field, comparator=comparator, value=value)

            if mapped_fields_count > 1:
                comparison_string += "&"
                mapped_fields_count -= 1
        return comparison_string

    @staticmethod
    def _is_reference_value(stix_field):
        return stix_field == 'src_ref.value' or stix_field == 'dst_ref.value'

    @staticmethod
    def _is_object_filterType(stix_object, stix_field):
        if (stix_object in REFERENCE_FILTER_TYPE) and (stix_field not in REFERENCE_EXCLUDE_FILTER_TYPE):
            return True
        else:
            return False

    @staticmethod
    def _check_filter_value_type(value, stix_object):
        """
        Function returning value type of event type object in double quotes
        :param value: str
        :return: string
        """
        event_object = ['event_type']
        if stix_object in event_object:
            return '"{}"'.format(value)
        else:
            return value

    @staticmethod
    def _lookup_comparison_operator(self, expression_operator):
        if str(expression_operator) not in self.comparator_lookup:
            raise NotImplementedError(
                "Comparison operator {} unsupported for verify connector".format(expression_operator.name))
        return self.comparator_lookup[str(expression_operator)]

    @classmethod
    def _format_start_stop_qualifier(self, expression, qualifier) -> str:
        """
        Convert a STIX start stop qualifier into a query string.
        """
        transformer = TimestampToMilliseconds()
        qualifier_split = qualifier.split("'")
        start = qualifier_split[1]
        stop = qualifier_split[3]
        # convert timepestamp to millisecond which will be passed to rest service
      
        start_epoach = self.get_epoch_time(start)
        stop_epoach = self.get_epoch_time(stop)
        qualified_query = "%s&from=%s&to=%s" % (
            expression, start_epoach, stop_epoach)
        return qualified_query

    def _parse_expression(self, expression, qualifier=None) -> Union[str, list]:
        if isinstance(expression, ComparisonExpression):  # Base Case
            # Resolve STIX Object Path to a field in the target Data Model
            stix_object, stix_field = expression.object_path.split(':')
            # Multiple data source fields may map to the same STIX Object
            mapped_fields_array = self.dmm.map_field(stix_object, stix_field)
            # Resolve the comparison symbol to use in the query string (usually just ':')
            comparator = self._lookup_comparison_operator(
                self, expression.comparator)

            # Some values are formatted differently based on how they're being compared
            if expression.comparator == ComparisonComparators.Equal or expression.comparator == ComparisonComparators.NotEqual:
                # Should be in single-quotes
                value = self._escape_value(expression.value)
                # check if belongs to event object type. This require sepecial treatment.
                value = self._check_filter_value_type(value, stix_object)
            elif expression.comparator == ComparisonComparators.In:
                in_string = expression.value.values if hasattr(
                    expression.value, 'values') else expression.value
                values = self._convert_list_string_in_condition(in_string)
                # apply escape value to remove unwanted char in string.
                value = self._escape_value(values)

            else:
                value = self._escape_value(expression.value)

            comparison_string = self._parse_mapped_fields(
                self, expression, value, comparator, stix_field, mapped_fields_array, stix_object)
            if(len(mapped_fields_array) > 1 and not self._is_reference_value(stix_field)):
                # More than one data source field maps to the STIX attribute, so group comparisons together.
                grouped_comparison_string = comparison_string
                comparison_string = grouped_comparison_string

            if expression.negated:
                comparison_string = self._negate_comparison(comparison_string)
            if qualifier is not None:
                return self._format_start_stop_qualifier(comparison_string, qualifier)
            else:
                return "{}".format(comparison_string)

        elif isinstance(expression, CombinedComparisonExpression):
            operator = self._lookup_comparison_operator(
                self, expression.operator)
            expression_01 = self._parse_expression(expression.expr1)
            expression_02 = self._parse_expression(expression.expr2)

            if not expression_01 or not expression_02:
                return ''
            if isinstance(expression.expr1, CombinedComparisonExpression):
                expression_01 = "{}".format(expression_01)
            if isinstance(expression.expr2, CombinedComparisonExpression):
                expression_02 = "{}".format(expression_02)

            query_string = "{}{}{}".format(
                expression_01, operator, expression_02)
            if qualifier is not None:
                return self._format_start_stop_qualifier(query_string, qualifier)
            else:
                return "{}".format(query_string)
        elif isinstance(expression, ObservationExpression):
            return self._parse_expression(expression.comparison_expression, qualifier)
        elif hasattr(expression, 'qualifier') and hasattr(expression, 'observation_expression'):
            if isinstance(expression.observation_expression, CombinedObservationExpression):
                operator = self._lookup_comparison_operator(
                    self, expression.observation_expression.operator)
                expression_01 = self._parse_expression(
                    expression.observation_expression.expr1)
                # qualifier only needs to be passed into the parse expression once since it will be the same for both expressions
                expression_02 = self._parse_expression(
                    expression.observation_expression.expr2, expression.qualifier)
                return "{} {} {}".format(expression_01, operator, expression_02)
            else:
                return self._parse_expression(expression.observation_expression.comparison_expression, expression.qualifier)
        elif isinstance(expression, CombinedObservationExpression):
            operator = self._lookup_comparison_operator(
                self, expression.operator)
            expression_01 = self._parse_expression(expression.expr1)
            expression_02 = self._parse_expression(expression.expr2)
            if not isinstance(expression_01, list):
                QueryStringPatternTranslator.QUERIES.extend([expression_01])
            if not isinstance(expression_02, list):
                QueryStringPatternTranslator.QUERIES.extend([expression_02])
            return QueryStringPatternTranslator.QUERIES
        elif isinstance(expression, Pattern):
            return self._parse_expression(expression.expression)
        else:
            raise RuntimeError("Unknown Recursion Case for expression={}, type(expression)={}".format(
                expression, type(expression)))

    def parse_expression(self, pattern: Pattern):
        return self._parse_expression(pattern)
    
    @staticmethod
    def get_epoch_time(timestamp):
        
        """
        Converting timestamp (YYYY-MM-DDThh:mm:ss.000Z) to 13-digit Unix time (epoch + milliseconds)
        :param timestamp: str, timestamp
        :return: int, epoch time
        """
        time_patterns = ['%Y-%m-%dT%H:%M:%SZ', '%Y-%m-%dT%H:%M:%S.%fZ']
        epoch = datetime(1970, 1, 1)
        for time_pattern in time_patterns:
            try:
                converted_time = int(((datetime.strptime(timestamp, time_pattern) - epoch).total_seconds()) * 1000)
                return converted_time
            except ValueError:
                pass
        raise NotImplementedError("cannot convert the timestamp {} to milliseconds".format(timestamp))


def translate_pattern(pattern: Pattern, data_model_mapping, options):
    # Query result limit and time range can be passed into the QueryStringPatternTranslator if supported by the data source.
    result_limit = options['result_limit']
    list_final_query = []
    # time_range = options['time_range']
    query = QueryStringPatternTranslator(
        pattern, data_model_mapping).translated
    query = query if isinstance(query, list) else [query]
    for each_query in query:
        base_query = f"{each_query}&size={result_limit}"
        list_final_query.append(base_query)

    return list_final_query
