import json
import re
from os import path
from datetime import datetime, timedelta
from stix_shifter_utils.utils import logger
from stix_shifter_utils.stix_translation.src.patterns.pattern_objects import ObservationExpression, \
    ComparisonExpression, ComparisonComparators, Pattern, CombinedComparisonExpression, CombinedObservationExpression

logger = logger.set_logger(__name__)

START_STOP_PATTERN = r"(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?Z)"
STOP_TIME = datetime.utcnow()
CONFIG_MAP_PATH = "json/config_map.json"
DEFAULT_LIMIT = 10000


class FileNotFoundException(Exception):
    pass


class QueryStringPatternTranslator:
    """
    comparator values to match with supported data source operators
    """

    def __init__(self, pattern: Pattern, data_model_mapper, options):

        logger.info("Darktrace Connector")
        self.dmm = data_model_mapper
        self.comparator_lookup = self.dmm.map_comparator()
        self.config_map = self.load_json(CONFIG_MAP_PATH)
        self.pattern = pattern
        self.options = options
        self.qualified_queries = []
        self.parse_expression(pattern)

    @staticmethod
    def load_json(rel_path_of_file):
        """
        Consumes a json file and returns a dictionary
        :param rel_path_of_file: str
        :return: dict
        """

        _json_path = path.dirname(path.realpath(__file__)) + "/" + rel_path_of_file
        try:
            if path.exists(_json_path):
                with open(_json_path, encoding='utf-8') as f_obj:
                    return json.load(f_obj)
            raise FileNotFoundException
        except FileNotFoundException as e:
            raise FileNotFoundError(f'{rel_path_of_file} not found') from e

    @staticmethod
    def _format_datetime(value):
        """
         Converts timestamp to epoch
        :param: value
        :return: int, converted epoch value
        """
        try:
            time_pattern = '%Y-%m-%dT%H:%M:%S.%fZ'
            epoch = datetime(1970, 1, 1)
            converted_time = int(((datetime.strptime(value, time_pattern) - epoch).total_seconds()) * 1000)
            return converted_time
        except ValueError:
            pass
        raise NotImplementedError(f'cannot convert the timestamp {value} to milliseconds')

    @staticmethod
    def _format_match(value, mapped_field_type):
        """
        Formats value in the event of match operation
        :param value, mapped_field_type
        :return formatted string type value
        """
        if mapped_field_type == "mac":
            raise NotImplementedError("MATCHES operator is not supported for mac type field")
        if mapped_field_type != "string":
            raise NotImplementedError("MATCHES operator is supported only for string type input")
        if '^' in value and value.index('^') != 0:
            raise NotImplementedError('^ symbol should be at the starting position of the expression')
        if '$' in value and value.index('$') != len(value) - 1:
            raise NotImplementedError('$ symbol should be at the ending position of the expression')
        value = re.escape(value).replace('/', "\\/").replace(':', "\\:")
        return '/' + value + '/'

    @staticmethod
    def _format_like(value, mapped_field_type):
        """
        Formatting value in the event of like operation
        :param value,mapped_fields_array
        :return: list
        """
        if mapped_field_type == "mac":
            raise NotImplementedError("LIKE operator is not supported for mac type field")
        if mapped_field_type != "string":
            raise NotImplementedError("LIKE operator is supported only for string type input")
        value = re.escape(value).replace('/', "\\/").replace(':', "\\:")
        return '*' + value + '*'

    @staticmethod
    def _format_greater_lesser(value, expression):
        """
        Formatting GreaterThanOrEqual and LessThanOrEqual
        :param value,expression
        :return: int
        """
        if isinstance(value, str) and not value.isnumeric():
            raise NotImplementedError(f"{expression.comparator.name} operator is not supported for string type input")

        if expression.comparator == ComparisonComparators.GreaterThanOrEqual:
            if isinstance(value, (int, float)):
                value = value - 1
            elif isinstance(value, str) and value.isnumeric():
                value = int(value) - 1
        elif expression.comparator == ComparisonComparators.LessThanOrEqual:
            if isinstance(value, (int, float)):
                value = value + 1
            elif isinstance(value, str) and value.isnumeric():
                value = int(value) + 1
        return value

    @staticmethod
    def _parse_time_range(qualifier, time_range):
        """
        Converts qualifier timestamp to epoch
        return: list of converted epoch values
        """
        try:
            compile_timestamp_regex = re.compile(START_STOP_PATTERN)
            converted_timestamp = []
            if qualifier and compile_timestamp_regex.search(qualifier):
                time_range_iterator = compile_timestamp_regex.finditer(qualifier)
                time_range_list = [each.group() for each in time_range_iterator]
            else:
                start_time = STOP_TIME - timedelta(minutes=time_range)
                converted_start_time = start_time.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
                # limit 3 digit value for millisecond
                converted_stop_time = STOP_TIME.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
                time_range_list = [converted_start_time, converted_stop_time]
            for timestamp in time_range_list:
                converted_time = QueryStringPatternTranslator._format_datetime(timestamp) / 1000
                converted_timestamp.append(converted_time)
            return converted_timestamp
        except (KeyError, IndexError, TypeError) as e:
            raise e

    def _check_mapped_field_type(self, mapped_field_array):
        """
        Returns the type of mapped field array
        :param mapped_field_array: list
        :return: str
        """
        mapped_field = mapped_field_array[0]
        mapped_field_type = "string"
        for key, value in self.config_map.items():
            if mapped_field in value and key in ["int_supported_fields", "mac_supported_fields",
                                                 "boolean_supported_fields"]:
                mapped_field_type = key.split('_')[0]
                break
        return mapped_field_type

    @staticmethod
    def _format_value_type(value, mapped_field_type):
        """
        check input value format that matches with the mapped field value type
        :param value
        :param mapped_field_type: str
        :return value
        """
        converted_value = str(value)
        if mapped_field_type == "int":
            if not converted_value.replace(".", "").isdigit():
                raise NotImplementedError(f'string type input - {value} is not supported for '
                                          f'integer type fields')
        return value

    @staticmethod
    def _eval_comparison_value(expression, mapped_field_type):
        """
        Function for parsing comparison expression value
        :param expression: expression object
        :return: formatted expression value
        """
        value = expression.value

        if expression.comparator == ComparisonComparators.In:
            value = ' OR '.join('"' + str(QueryStringPatternTranslator._format_value_type(row, mapped_field_type)) + '"'
                                for row in value.values)
            return '(' + value + ')'
        elif expression.comparator == ComparisonComparators.Like:
            return QueryStringPatternTranslator._format_like(value, mapped_field_type)
        elif expression.comparator == ComparisonComparators.Matches:
            return QueryStringPatternTranslator._format_match(value, mapped_field_type)
        elif expression.comparator in [ComparisonComparators.GreaterThan, ComparisonComparators.GreaterThanOrEqual,
                                       ComparisonComparators.LessThan, ComparisonComparators.LessThanOrEqual]:
            value = QueryStringPatternTranslator._format_value_type(value, mapped_field_type)
            return QueryStringPatternTranslator._format_greater_lesser(value, expression)

        if mapped_field_type == 'int':
            return QueryStringPatternTranslator._format_value_type(value, mapped_field_type)
        else:
            return '"' + str(value) + '"'

    def _add_qualifier(self, query, qualifier):
        """
        Convert the qualifier into epoch time and
        append in the query.
        params: query : str
        params: qualifier
        return: query : str
        """
        time_range = QueryStringPatternTranslator._parse_time_range(qualifier, self.options['time_range'])
        query += f" AND (@fields.epochdate :>{time_range[0]} AND @fields.epochdate :<{time_range[1]})"
        query = '(' + query + ')'
        return query

    @staticmethod
    def _create_single_comparison_query(comparator, value, mapped_fields_array, negated):
        """
        creates individual query for every comparison expression
        :param comparator: str
        :param value: list
        :param mapped_fields_array : list
        :param negated: str
        :return : str
        """
        query = ''

        if comparator == 'NOT':
            negated = True
            comparator = ':'

        # constructing query using from_stix values
        for facet_name in mapped_fields_array:

            if "@fields." in query:
                query += ' OR '

            if negated:
                negated_query = "@fields." + facet_name + ":* AND NOT "
                query += '(' + negated_query + "@fields." + facet_name + comparator + str(value) + ')'
                continue

            query += "@fields." + facet_name + comparator + str(value)

        if query.count('fields') > 1:
            return '(' + query + ')'
        return query

    def _parse_expression(self, expression, qualifier=None):
        """
         Formation of Darktrace query from ANTLR parsing expression
        :param expression: expression object, ANTLR parsed expression object
        :param qualifier: str, default in None
        :return :None or str
        """
        if isinstance(expression, ComparisonExpression):  # Base Case
            stix_object, stix_field = expression.object_path.split(':')
            mapped_fields_array = self.dmm.map_field(stix_object, stix_field)
            comparator = self.comparator_lookup[str(expression.comparator)]
            mapped_field_type = self._check_mapped_field_type(mapped_fields_array)
            value = QueryStringPatternTranslator._eval_comparison_value(expression, mapped_field_type)
            query = self._create_single_comparison_query(comparator, value, mapped_fields_array, expression.negated)

            if qualifier is not None:
                query = self._add_qualifier(query, qualifier)

            return query

        elif isinstance(expression, CombinedComparisonExpression):
            expression_01 = self._parse_expression(expression.expr1)
            expression_02 = self._parse_expression(expression.expr2)

            if not expression_01 or not expression_02:
                return ''

            query = f"({expression_01} {self.comparator_lookup[str(expression.operator)]} {expression_02})"

            if qualifier is not None:
                query = self._add_qualifier(query, qualifier)
            return query

        elif isinstance(expression, ObservationExpression):
            query = self._parse_expression(expression.comparison_expression, qualifier)
            return query

        elif hasattr(expression, 'qualifier') and hasattr(expression, 'observation_expression'):
            if isinstance(expression.observation_expression, CombinedObservationExpression):
                exp1 = self._parse_expression(expression.observation_expression.expr1)
                exp2 = self._parse_expression(expression.observation_expression.expr2)
                query = f"({exp1} {self.comparator_lookup[str(expression.observation_expression.operator)]} {exp2})"
                query = self._add_qualifier(query, expression.qualifier)
            else:
                query = self._parse_expression(expression.observation_expression.comparison_expression,
                                               expression.qualifier)
            return query

        elif isinstance(expression, CombinedObservationExpression):
            expression_01 = self._parse_expression(expression.expr1)
            expression_02 = self._parse_expression(expression.expr2)

            if expression_01 and expression_02:
                return f"({expression_01} {self.comparator_lookup[str(expression.operator)]} {expression_02})"
            elif expression_01:
                return f"{expression_01}"
            elif expression_02:
                return f"{expression_02}"

            return ''

        elif isinstance(expression, Pattern):
            return self._parse_expression(expression.expression)
        else:
            raise RuntimeError(f'Unknown Recursion Case for expression={expression}, '
                               f'type(expression)={type(expression)}')

    def parse_expression(self, pattern: Pattern):
        """
         Formation of Darktrace query from ANTLR parsing expression.
        :param pattern: expression object, ANTLR parsed expression object
        """

        darktrace_query = self._parse_expression(pattern)
        pattern = r"\@fields\.epochdate\s\:[^0-9](\d{0,10}.\d{0,3})"
        qualifiers = re.findall(pattern, darktrace_query)

        if not qualifiers:  # Adding default qualifier if qualifier is not present.
            darktrace_query = self._add_qualifier(darktrace_query, None)
            qualifiers = re.findall(pattern, darktrace_query)

        start = datetime.utcfromtimestamp(float(min(qualifiers))).strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        stop = datetime.utcfromtimestamp(float(max(qualifiers))).strftime('%Y-%m-%dT%H:%M:%S.%fZ')

        if self.options['result_limit'] > DEFAULT_LIMIT:
            self.options['result_limit'] = DEFAULT_LIMIT

        query = {"search": darktrace_query, "fields": [],
                 "timeframe": "custom", "time": {"from": start, "to": stop}, "size": self.options['result_limit']}

        self.qualified_queries.append(query)


def translate_pattern(pattern: Pattern, data_model_mapping, options):
    """
    Conversion of ANTLR pattern to Darktrace query
    :param pattern: expression object, ANTLR parsed expression object
    :param data_model_mapping: DataMapper object, mapping object obtained by parsing json
    :param options: dict, time_range defaults to 5
    :return: list, Darktrace queries
    """
    translated_query_strings = QueryStringPatternTranslator(pattern, data_model_mapping, options)
    queries = translated_query_strings.qualified_queries
    return queries
