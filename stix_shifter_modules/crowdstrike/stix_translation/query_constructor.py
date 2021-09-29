from stix_shifter_utils.stix_translation.src.patterns.pattern_objects import ObservationExpression, \
    ComparisonExpression, \
    ComparisonExpressionOperators, ComparisonComparators, Pattern, \
    CombinedComparisonExpression, CombinedObservationExpression, ObservationOperators, StartStopQualifier
from datetime import datetime, timedelta


class CSQueryStringPatternTranslator:
    QUERIES = []
    """
    Stix to FQL query translation
    """
    comparator_lookup = {
        ComparisonExpressionOperators.And: "+",
        ComparisonExpressionOperators.Or: ",",
        ComparisonComparators.Equal: ":",
        ComparisonComparators.NotEqual: ":!",
        ComparisonComparators.GreaterThan: ":>",
        ComparisonComparators.GreaterThanOrEqual: ":>=",
        ComparisonComparators.LessThan: ":<",
        ComparisonComparators.LessThanOrEqual: ":<=",
    }

    def __init__(self, pattern: Pattern, data_model_mapper, time_range):
        # self.logger = logger.set_logger(__name__)
        self.dmm = data_model_mapper
        self.pattern = pattern
        self.time_range = time_range  # filter results to last x minutes
        self.translated = self.parse_expression(pattern)
        self.queries = []
        self.queries.extend(self.translated)

    @staticmethod
    def _escape_value(value, comparator=None) -> str:
        if isinstance(value, str):
            return '{}'.format(
                value.replace('\\', '\\\\').replace('\"', '\\"').replace('(', '\\(').replace(')', '\\)').replace(
                    ' ', '\\ '))
        else:
            return value

    @staticmethod
    def _to_cs_timestamp(ts: str) -> str:
        stripped = ts[2:-2]
        if '.' in stripped:
            stripped = stripped.split('.', 1)[0]
        return stripped

    def _format_start_stop_qualifier(self, expression, qualifier: StartStopQualifier) -> str:
        start = self._to_cs_timestamp(qualifier.start)
        stop = self._to_cs_timestamp(qualifier.stop)

        start_stop_query = "(behaviors.timestamp:>= '{}' + behaviors.timestamp:<= '{}')".format(start, stop)

        return "({}) + {}".format(expression, start_stop_query)

    def _parse_expression(self, expression, qualifier=None):
        if isinstance(expression, ComparisonExpression):
            # Base Case
            # Resolve STIX Object Path to a field in the target Data Model
            stix_object, stix_field = expression.object_path.split(':')

            mapped_fields_array = self.dmm.map_field(stix_object, stix_field)
            mapped_fields_count = len(mapped_fields_array)
            query_string = ""
            comparator = self.comparator_lookup[expression.comparator]
            if expression.negated and expression.comparator == ComparisonComparators.Equal:
                comparator = self._get_negate_comparator()

            elif expression.comparator == ComparisonComparators.NotEqual and not expression.negated:
                comparator = self._get_negate_comparator()

            value = self._escape_value(expression.value)

            for mapped_field in mapped_fields_array:
                # Handle negate exp
                mapped_field_query_str = "{mapped_field}{comparator} '{value}'".format(mapped_field=mapped_field,
                                                                                  comparator=comparator, value=value)
                if mapped_fields_count > 1:
                    mapped_field_query_str += self.comparator_lookup[ComparisonExpressionOperators.Or]
                    mapped_fields_count -= 1

                query_string += mapped_field_query_str

            if qualifier is not None:
                if isinstance(qualifier, StartStopQualifier):
                    query_string = self._format_start_stop_qualifier(query_string, qualifier)
                else:
                    raise RuntimeError("Unknown Qualifier: {}".format(qualifier))

            return '({})'.format(query_string)

        elif isinstance(expression, CombinedComparisonExpression):
            # Wrap nested combined comparison expressions in parentheses
            f1 = "({})" if isinstance(expression.expr2, CombinedComparisonExpression) else "{}"
            f2 = "({})" if isinstance(expression.expr1, CombinedComparisonExpression) else "{}"

            query_string = (f1 + " {} " + f2).format(self._parse_expression(expression.expr2),
                                                     self.comparator_lookup[expression.operator],
                                                     self._parse_expression(expression.expr1))
            if qualifier is not None:
                if isinstance(qualifier, StartStopQualifier):
                    return self._format_start_stop_qualifier(query_string, qualifier)
                else:
                    raise RuntimeError("Unknown Qualifier: {}".format(qualifier))
            else:
                return "{}".format(query_string)
        elif isinstance(expression, ObservationExpression):
            query_string = self._parse_expression(expression.comparison_expression, qualifier=qualifier)
            return query_string
        elif isinstance(expression, CombinedObservationExpression):
            expr1 = self._parse_expression(expression.expr1, qualifier=qualifier)
            expr2 = self._parse_expression(expression.expr2, qualifier=qualifier)
            if (not isinstance(expr1, list)):
                CSQueryStringPatternTranslator.QUERIES.extend([expr1])
            if (not isinstance(expr2, list)):
                CSQueryStringPatternTranslator.QUERIES.extend([expr2])
            return CSQueryStringPatternTranslator.QUERIES
        elif isinstance(expression, Pattern):
            return self._parse_expression(expression.expression)
        elif hasattr(expression, 'qualifier') and hasattr(expression, 'observation_expression'):
            return self._parse_expression(expression.observation_expression, expression)
        else:
            raise RuntimeError("Unknown Recursion Case for expression={}, type(expression)={}".format(
                expression, type(expression)))

    def _get_negate_comparator(self):
        return self.comparator_lookup[ComparisonComparators.NotEqual]

    def _add_default_timerange(self, query):
        if self.time_range and 'behaviors.timestamp' not in query:
            d = (datetime.today() - timedelta(hours=0, minutes=self.time_range)).isoformat()
            n_query = "(({}) + behaviors.timestamp:> '{}')".format(query, d)
            return n_query

        return query

    def _add_default_timerange_to_queries(self, queries):
        n_queries = list()
        if not isinstance(queries, list):
            queries = [queries]
        for q in queries:
            n_queries.append(self._add_default_timerange(q))

        return n_queries

    def parse_expression(self, pattern: Pattern):
        queries = self._parse_expression(pattern)
        return self._add_default_timerange_to_queries(queries)


def translate_pattern(pattern: Pattern, data_model_mapping, options):
    time_range = options['time_range']

    translated_statements_lst = CSQueryStringPatternTranslator(pattern, data_model_mapping, time_range)
    translated_statements = ",".join(translated_statements_lst.queries)
    return translated_statements
