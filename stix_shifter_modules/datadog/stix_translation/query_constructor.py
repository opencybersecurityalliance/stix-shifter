import json
import time
from stix_shifter_utils.stix_translation.src.patterns.pattern_objects import ObservationExpression, \
    ComparisonExpression, \
    ComparisonExpressionOperators, ComparisonComparators, Pattern, \
    CombinedComparisonExpression, CombinedObservationExpression, ObservationOperators
from stix_shifter_utils.stix_translation.src.utils.transformers import TimestampToMilliseconds
from stix_shifter_utils.stix_translation.src.json_to_stix import observable
import logging
import re
from typing import Union

# Source and destination reference mapping for ip and mac addresses.
# Change the keys to match the data source fields. The value array indicates the possible data type that can come into from field.
REFERENCE_DATA_TYPES = {}

logger = logging.getLogger(__name__)

class QueryStringPatternTranslator:
    QUERIES = []

    def __init__(self, pattern: Pattern, data_model_mapper):
        self.dmm = data_model_mapper
        self.comparator_lookup = self.dmm.map_comparator()
        self.pattern = pattern
        self.translated = self.parse_expression(pattern)

    @staticmethod
    def _format_set(values):
        gen = values.element_iterator()
        return [QueryStringPatternTranslator._escape_value(value) for value in gen]

    @staticmethod
    def _format_equality(value) -> str:
        return '\'{}\''.format(value)

    @staticmethod
    def _escape_value(value, comparator=None) -> str:
        if isinstance(value, str):
            return '{}'.format(value.replace('\\', '\\\\').replace('\"', '\\"').replace('(', '\\(').replace(')', '\\)'))
        else:
            return value

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
            return "{mapped_field} {comparator} {value}".format(
                mapped_field=mapped_field, comparator=comparator, value=value)

    @staticmethod
    def _parse_mapped_fields(self, expression, value, comparator, stix_field, mapped_fields_array):
        comparison_string = ""
        is_reference_value = self._is_reference_value(stix_field)
        # Need to use expression.value to match against regex since the passed-in value has already been formated.
        value_type = self._check_value_type(expression.value) if is_reference_value else None
        mapped_fields_count = 1 if is_reference_value else len(mapped_fields_array)

        for mapped_field in mapped_fields_array:
            if is_reference_value:
                parsed_reference = self._parse_reference(self, stix_field, value_type, mapped_field, value, comparator)
                if not parsed_reference:
                    continue
                comparison_string += parsed_reference
            else:
                comparison_string += "'{mapped_field}' {comparator} {value}".format(mapped_field=mapped_field,
                                                                                    comparator=comparator, value=value)

            if mapped_fields_count > 1:
                comparison_string += " OR "
                mapped_fields_count -= 1
        return comparison_string

    @staticmethod
    def _is_reference_value(stix_field):
        return stix_field == 'src_ref.value' or stix_field == 'dst_ref.value'

    @staticmethod
    def _lookup_comparison_operator(self, expression_operator):
        if str(expression_operator) not in self.comparator_lookup:
            raise NotImplementedError(
                "Comparison operator {} unsupported for Datadog connector".format(expression_operator.name))
        return self.comparator_lookup[str(expression_operator)]

    @staticmethod
    def join_duplicate_keys(ordered_pairs):
        d = {}
        for k, v in ordered_pairs:
            if k in d:
                if type(d[k]) == list:
                    d[k].append(v)
                else:
                    newlist = [d[k], v]
                    d[k] = newlist
            else:
                d[k] = v
        return d

    def convert_to_json(self, expressions):
        """Convert to json and modify some keys value
        :param expressions: string, queries
        :return: final_list, list"""
        final_list = []
        query_str = dict()
        for expression in expressions:
            newdict = json.loads(expression, object_pairs_hook=QueryStringPatternTranslator.join_duplicate_keys)
            if "source" in newdict and isinstance(newdict["source"], list):
                newdict["source"] = ",".join(map(str, newdict["source"]))
            if "tags" in newdict and isinstance(newdict["tags"], list):
                newdict["tags"] = ",".join(map(str, newdict["tags"]))
            # Converting into integer
            keys = ["start", "end", "date_happened", "monitor_id", "id"]
            for key in keys:
                if isinstance(newdict.get(key, 1), str):
                    newdict[key] = int(newdict[key])
                elif isinstance(newdict.get(key, 1), list):
                    newdict[key] = [int(i) for i in newdict[key]]
            # in case of multiple priority taking only first value as datasource support only one
            if "priority" in newdict and isinstance(newdict["priority"], list):
                newdict["priority"] = newdict["priority"][0]
            query_str['query'] = newdict
            final_list.append(json.dumps(query_str))
        return final_list

    def matched(self, queries, time_range):
        """To add default parameters (start,end) and divide query based on OR
        :param queries: string, queries
        :param time_range: int, minutes
        :return: final_list, list"""
        final_list = []
        end = int(time.time())
        # default last 5 minutes (300 sec)
        start = end - (time_range * 60)
        for query in queries:
            start_flag = re.search("start' :(.+?)AND", query)
            end_flag = re.search("end' :(.+?)$", query)
            if start_flag:
                start = start_flag.group(1).strip()
            if end_flag:
                end = end_flag.group(1).strip()
            if "OR" in query:
                or_list = query.split("OR")
                for expr in or_list:
                    expr = self.query_builder(expr, start, end, time_range)
                    final_list.append(expr)
            else:
                expr = self.query_builder(query, start, end, time_range)
                final_list.append(expr)
        return final_list

    @staticmethod
    def query_builder(query, start, end, time_range):
        if all(x in query for x in ["start", "end"]):
            expr = '{%s}' % query
        elif "start" in query:
            expr = '{%s AND "end" : %s}' % (query, end)
        elif "end" in query:
            start = int(end.strip("'")) - (time_range * 60)
            expr = '{%s AND "start" : %s}' % (query, start)
        else:
            expr = '{%s AND "start" : %s AND "end" : %s}' % (query, start, end)
        expr = expr.replace("'", '"').replace("AND", ",")
        return expr

    @classmethod
    def _format_start_stop_qualifier(self, expression, qualifier) -> str:
        """Convert a STIX start stop qualifier into a query string.
        """
        transformer = TimestampToMilliseconds()
        qualifier_split = qualifier.split("'")
        start = transformer.transform(qualifier_split[1]) // 1000
        stop = transformer.transform(qualifier_split[3]) // 1000
        qualified_query = "%s AND 'start' : %s AND 'end' : %s" % (expression, start, stop)
        return qualified_query

    def _parse_expression(self, expression, qualifier=None) -> Union[str, list]:
        if isinstance(expression, ComparisonExpression):  # Base Case
            # Resolve STIX Object Path to a field in the target Data Model
            stix_object, stix_field = expression.object_path.split(':')
            # Multiple data source fields may map to the same STIX Object
            mapped_fields_array = self.dmm.map_field(stix_object, stix_field)
            # Resolve the comparison symbol to use in the query string (usually just ':')
            comparator = self._lookup_comparison_operator(self, expression.comparator)

            if stix_field in ['start','end', "time_observed"]:
                transformer = TimestampToMilliseconds()
                expression.value = transformer.transform(expression.value) // 1000

            # Some values are formatted differently based on how they're being compared
            # should be (x, y, z, ...)
            if expression.comparator == ComparisonComparators.In:
                value = self._format_set(expression.value)
            elif expression.comparator == ComparisonComparators.Equal or expression.comparator == ComparisonComparators.NotEqual:
                # Should be in single-quotes
                value = self._format_equality(expression.value)
            else:
                value = self._escape_value(expression.value)

            comparison_string = self._parse_mapped_fields(self, expression, value, comparator, stix_field,
                                                          mapped_fields_array)
            # if(len(mapped_fields_array) > 1 and not self._is_reference_value(stix_field)):
            #     # More than one data source field maps to the STIX attribute, so group comparisons together.
            #     grouped_comparison_string = comparison_string
            #     comparison_string = grouped_comparison_string

            if expression.negated:
                comparison_string = self._negate_comparison(comparison_string)
            if qualifier is not None:
                return self._format_start_stop_qualifier(comparison_string, qualifier)
            else:
                return "{}".format(comparison_string)

        elif isinstance(expression, CombinedComparisonExpression):
            operator = self._lookup_comparison_operator(self, expression.operator)
            expression_01 = self._parse_expression(expression.expr1)
            expression_02 = self._parse_expression(expression.expr2)
            if not expression_01 or not expression_02:
                return ''
            if isinstance(expression.expr1, CombinedComparisonExpression):
                expression_01 = "{}".format(expression_01)
            if isinstance(expression.expr2, CombinedComparisonExpression):
                expression_02 = "{}".format(expression_02)
            query_string = "{} {} {}".format(expression_01, operator, expression_02)
            if qualifier is not None:
                return self._format_start_stop_qualifier(query_string, qualifier)
            else:
                return "{}".format(query_string)
        elif isinstance(expression, ObservationExpression):
            return self._parse_expression(expression.comparison_expression, qualifier)
        elif hasattr(expression, 'qualifier') and hasattr(expression, 'observation_expression'):
            if isinstance(expression.observation_expression, CombinedObservationExpression):
                operator = self._lookup_comparison_operator(self, expression.observation_expression.operator)
                expression_01 = self._parse_expression(expression.observation_expression.expr1)
                # qualifier only needs to be passed into the parse expression once since it will be the same for both expressions
                expression_02 = self._parse_expression(expression.observation_expression.expr2, expression.qualifier)
                return "{} {} {}".format(expression_01, operator, expression_02)
            else:
                return self._parse_expression(expression.observation_expression.comparison_expression,
                                              expression.qualifier)
        elif isinstance(expression, CombinedObservationExpression):
            queries = []
            operator = self._lookup_comparison_operator(self, expression.operator)
            expression_01 = self._parse_expression(expression.expr1)
            expression_02 = self._parse_expression(expression.expr2)
            if not isinstance(expression_01, list):
                queries.extend([expression_01])
            if not isinstance(expression_02, list):
                queries.extend([expression_02])
            return queries
        elif isinstance(expression, Pattern):
            return self._parse_expression(expression.expression)
        else:
            raise RuntimeError("Unknown Recursion Case for expression={}, type(expression)={}".format(
                expression, type(expression)))

    def parse_expression(self, pattern: Pattern):
        return self._parse_expression(pattern)


def translate_pattern(pattern: Pattern, data_model_mapping, options):
    time_range = options['time_range']
    payload = []
    querys = dict()
    datadog_translator = QueryStringPatternTranslator(pattern, data_model_mapping)
    expression = datadog_translator.translated
    expression = expression if isinstance(expression, list) else [expression]
    # To add default parameters (start,end) and divide query based on OR comparison operator
    query = datadog_translator.matched(expression, time_range)
    # Convert to json and modify some keys value
    query = datadog_translator.convert_to_json(query)
    for trans_query in query:
        querys = json.loads(trans_query)
        querys["source"] = data_model_mapping.dialect
        payload.append(json.dumps(querys))
    return payload
