import logging
import datetime
import json
import re

logger = logging.getLogger(__name__)

from stix2patterns_translator.pattern_objects import ObservationExpression, ComparisonExpression, \
    ComparisonExpressionOperators, ComparisonComparators, Pattern, \
    CombinedComparisonExpression, CombinedObservationExpression, ObservationOperators
from stix2patterns_translator.errors import SearchFeatureNotSupportedError

from stix_shifter.src.transformers import TimestampToEpoch, ValueTransformer


def _fetch_network_protocol_mapping():
    try:
        map_file = open(
            'stix_shifter/src/modules/qradar/json/network_protocol_map.json').read()
        map_data = json.loads(map_file)
        return map_data
    except Exception as ex:
        print('exception in reading mapping file:', ex)
        return {}


class AqlQueryStringPatternTranslator:
    comparator_lookup = {
        ComparisonExpressionOperators.And: "AND",
        ComparisonExpressionOperators.Or: "OR",
        ComparisonComparators.GreaterThan: ">",
        ComparisonComparators.GreaterThanOrEqual: ">=",
        ComparisonComparators.LessThan: "<",
        ComparisonComparators.LessThanOrEqual: "<=",
        ComparisonComparators.Equal: "=",
        ComparisonComparators.NotEqual: "!=",
        ComparisonComparators.Like: "LIKE",
        ComparisonComparators.In: "IN",
        ComparisonComparators.Matches: 'MATCHES',
        ObservationOperators.Or: 'OR',
        # Treat AND's as OR's -- Unsure how two ObsExps wouldn't cancel each other out.
        ObservationOperators.And: 'OR'
    }

    def __init__(self, pattern: Pattern, data_model_mapper):
        self.dmm = data_model_mapper
        self.pattern = pattern
        self.parsed_pattern = []
        self.translated = self.parse_expression(pattern)

        query_split = self.translated.split("split")
        if len(query_split) > 1:
            # remove empty strings in the array
            query_array = list(map(lambda x: x.rstrip(), list(filter(None, query_split))))
            # removing leading AND/OR
            query_array = list(map(lambda x: re.sub("^\s(OR|AND)\s", "", x), query_array))
            # transform time format from '2014-04-25T15:51:20Z' into '2014-04-25 15:51:20'
            t_pattern = "((?<=START'\d{4}-\d{2}-\d{2})(T))|((?<=STOP'\d{4}-\d{2}-\d{2})(T))"
            query_array = list(map(lambda x: re.sub(t_pattern, " ", x), query_array))
            r_pattern = "((?<=\d{2}:\d{2}:\d{2})(Z))"
            query_array = list(map(lambda x: re.sub(r_pattern, "", x), query_array))
            self.queries = query_array
        else:
            self.queries = query_split

    @staticmethod
    def _format_set(values) -> str:
        gen = values.element_iterator()
        return "({})".format(' OR '.join([AqlQueryStringPatternTranslator._escape_value(value) for value in gen]))

    @staticmethod
    def _format_match(value) -> str:
        raw = AqlQueryStringPatternTranslator._escape_value(value)
        if raw[0] == "^":
            raw = raw[1:]
        else:
            raw = ".*" + raw
        if raw[-1] == "$":
            raw = raw[0:-1]
        else:
            raw = raw + ".*"
        return "\'{}\'".format(raw)

    @staticmethod
    def _format_equality(value) -> str:
        return '\'{}\''.format(value)

    @staticmethod
    def _format_like(value) -> str:
        value = value.replace('%', '*')
        value = value.replace('_', '?')
        return AqlQueryStringPatternTranslator._escape_value(value)

    @staticmethod
    def _escape_value(value, comparator=None) -> str:
        if isinstance(value, str):
            return '{}'.format(value.replace('\\', '\\\\').replace('\"', '\\"').replace('(', '\\(').replace(')', '\\)'))
        else:
            return value

    @staticmethod
    def _negate_comparison(comparison_string):
        return "NOT({})".format(comparison_string)

    def _parse_expression(self, expression, qualifier=None) -> str:
        if isinstance(expression, ComparisonExpression):  # Base Case
            # Resolve STIX Object Path to a field in the target Data Model
            stix_object, stix_field = expression.object_path.split(':')
            # Multiple QRadar fields may map to the same STIX Object
            mapped_fields_array = self.dmm.map_field(stix_object, stix_field)
            # Resolve the comparison symbol to use in the query string (usually just ':')
            comparator = self.comparator_lookup[expression.comparator]
            original_stix_value = expression.value

            if stix_field == 'protocols[*]':
                map_data = _fetch_network_protocol_mapping()
                try:
                    expression.value = map_data[expression.value.lower()]
                except Exception as protocol_key:
                    raise KeyError(
                        "Network protocol {} is not supported.".format(protocol_key))
            elif stix_field == 'start' or stix_field == 'end':
                transformer = TimestampToEpoch()
                expression.value = transformer.transform(expression.value)

            # Some values are formatted differently based on how they're being compared
            if expression.comparator == ComparisonComparators.Matches:  # needs forward slashes
                value = self._format_match(expression.value)
            # should be (x, y, z, ...)
            elif expression.comparator == ComparisonComparators.In:
                value = self._format_set(expression.value)
            elif expression.comparator == ComparisonComparators.Equal or expression.comparator == ComparisonComparators.NotEqual:
                # Should be in single-quotes
                value = self._format_equality(expression.value)
            # '%' -> '*' wildcard, '_' -> '?' single wildcard
            elif expression.comparator == ComparisonComparators.Like:
                value = self._format_like(expression.value)
            else:
                value = self._escape_value(expression.value)

            self.parsed_pattern.append({'attribute': expression.object_path, 'comparison_operator': comparator, 'value': original_stix_value})

            comparison_string = ""
            mapped_fields_count = len(mapped_fields_array)
            for mapped_field in mapped_fields_array:
                comparison_string += "{mapped_field} {comparator} {value}".format(
                    mapped_field=mapped_field, comparator=comparator, value=value)
                if (mapped_fields_count > 1):
                    comparison_string += " OR "
                    mapped_fields_count -= 1

            if(len(mapped_fields_array) > 1):
                # More than one AQL field maps to the STIX attribute so group the ORs.
                grouped_comparison_string = "(" + comparison_string + ")"
                comparison_string = grouped_comparison_string

            if expression.comparator == ComparisonComparators.NotEqual:
                comparison_string = self._negate_comparison(comparison_string)

            if expression.negated:
                comparison_string = self._negate_comparison(comparison_string)
            if qualifier is not None:
                return "{comparison} {qualifier} split".format(comparison=comparison_string, qualifier=qualifier)
            else:
                return "{comparison}".format(comparison=comparison_string)

        elif isinstance(expression, CombinedComparisonExpression):
            query_string = "{} {} {}".format(self._parse_expression(expression.expr1),
                                             self.comparator_lookup[expression.operator],
                                             self._parse_expression(expression.expr2))
            if qualifier is not None:
                return "{query_string} {qualifier} split".format(query_string=query_string, qualifier=qualifier)
            else:
                return "{query_string}".format(query_string=query_string)
        elif isinstance(expression, ObservationExpression):
            return self._parse_expression(expression.comparison_expression, qualifier)
        elif hasattr(expression, 'qualifier') and hasattr(expression, 'observation_expression'):
            if isinstance(expression.observation_expression, CombinedObservationExpression):
                operator = self.comparator_lookup[expression.observation_expression.operator]
                # qualifier only needs to be passed into the parse expression once since it will be the same for both expressions
                return "{expr1} {operator} {expr2}".format(expr1=self._parse_expression(expression.observation_expression.expr1),
                                                           operator=operator,
                                                           expr2=self._parse_expression(expression.observation_expression.expr2, expression.qualifier))
            else:
                return self._parse_expression(expression.observation_expression.comparison_expression, expression.qualifier)
        elif isinstance(expression, CombinedObservationExpression):
            operator = self.comparator_lookup[expression.operator]
            return "{expr1} {operator} {expr2}".format(expr1=self._parse_expression(expression.expr1),
                                                       operator=operator,
                                                       expr2=self._parse_expression(expression.expr2))
        elif isinstance(expression, Pattern):
            return "{expr}".format(expr=self._parse_expression(expression.expression))
        else:
            raise RuntimeError("Unknown Recursion Case for expression={}, type(expression)={}".format(
                expression, type(expression)))

    def parse_expression(self, pattern: Pattern):
        return self._parse_expression(pattern)


def translate_pattern(pattern: Pattern, data_model_mapping):
    x = AqlQueryStringPatternTranslator(pattern, data_model_mapping)
    select_statement = x.dmm.map_selections()
    queries = []
    for query in x.queries:
        queries.append("SELECT {select_statement} FROM events WHERE {where_clause}".format(select_statement=select_statement, where_clause=query))
    return {'aql_queries': queries, 'parsed_stix': x.parsed_pattern}
