import json
import re
from os import path
from pyparsing import nestedExpr, White
from datetime import datetime, timedelta
from stix_shifter_utils.utils import logger
from stix_shifter_utils.stix_translation.src.patterns.pattern_objects import ObservationExpression, \
    ComparisonExpression, ComparisonComparators, Pattern, CombinedComparisonExpression, CombinedObservationExpression

logger = logger.set_logger(__name__)

START_STOP_PATTERN = r"(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?Z)"
STOP_TIME = datetime.utcnow()
CONFIG_MAP_PATH = "json/config_map.json"

# API query limit is 1024 (MAX_QUERY_LENGTH+TIMESTAMP_LENGTH)
MAX_QUERY_LENGTH = 924
TIMESTAMP_LENGTH = 100


class FileNotFoundException(Exception):
    pass


class QueryStringPatternTranslator:
    """
    comparator values to match with supported data source operators
    """

    def __init__(self, pattern: Pattern, data_model_mapper, options):

        logger.info("Vectra Connector")
        self.dmm = data_model_mapper
        self.comparator_lookup = self.dmm.map_comparator()
        self.config_map = self.load_json(CONFIG_MAP_PATH)
        self.pattern = pattern
        self.options = options
        self.qualified_queries = []
        self.parse_expression(pattern)

    @staticmethod
    def load_json(rel_path_of_file):
        """ Consumes a json file and returns a dictionary
        :param rel_path_of_file: str
        :return: dict """
        _json_path = path.dirname(path.realpath(__file__)) + "/" + rel_path_of_file
        try:
            if path.exists(_json_path):
                with open(_json_path, encoding='utf-8') as f_obj:
                    return json.load(f_obj)
            raise FileNotFoundException
        except FileNotFoundException as e:
            raise FileNotFoundError(f'{rel_path_of_file} not found') from e

    def _format_set(self, values, mapped_field_type, expression) -> list:
        """
        Formats value in the event of set operation
        :param values: list
        :param mapped_field_type: str
        :param expression: object
        :return formatted value
        """
        gen = values.element_iterator()
        formatted_values = []
        for value in gen:
            value = self._check_value_comparator_support(value, expression.comparator, mapped_field_type)
            formatted_value = QueryStringPatternTranslator._format_equality(
                QueryStringPatternTranslator._format_value_type(value, mapped_field_type))
            formatted_values.append(formatted_value)
        return formatted_values

    @staticmethod
    def _format_match(value, mapped_field_type) -> str:
        """
        Formats value in the event of match operation
        :param value, mapped_field_type
        :return formatted string type value
        """
        if mapped_field_type != "string":
            raise NotImplementedError("MATCHES operator is supported only for string type input")
        if '^' in value and value.index('^') != 0:
            raise NotImplementedError('^ symbol should be at the starting position of the expression')
        if '$' in value and value.index('$') != len(value) - 1:
            raise NotImplementedError('$ symbol should be at the ending position of the expression')
        if ' ' in value:
            raise NotImplementedError('MATCHES operator is not supported for value contains spaces')
        value = QueryStringPatternTranslator._escape_value(value)
        return value + '*'

    @staticmethod
    def _format_equality(value) -> str:
        """
        Formats value in the event of equality operation
        :param value
        :return formatted value
        """
        return f'\"{str(value)}\"'

    @staticmethod
    def _format_like(value, mapped_field_type) -> str:
        """
        Formatting value in the event of like operation
        :param value,mapped_fields_array
        :return: list
        """
        if mapped_field_type != "string":
            raise NotImplementedError("LIKE operator is supported only for string type input")
        if ' ' in value:
            raise NotImplementedError('LIKE operator is not supported for value contains spaces')
        return QueryStringPatternTranslator._escape_value(value)

    @staticmethod
    def _escape_value(value) -> str:
        """
        adds escape characters to string and regex value
        :param value
        :return formatted value
        """
        if isinstance(value, str):
            value = value.replace('\\', '\\\\').replace('\"', '\\"')
        return value

    @staticmethod
    def _format_datetime(value) -> str:
        """
         format the date
        :param: value: str
        :return: converted_time: str
        """
        try:
            time_pattern = '%Y-%m-%dT%H:%M:%S.%fZ'
            if re.search(r"\d{4}(-\d{2}){2}T\d{2}(:\d{2}){2}Z", str(value)):  # without milli seconds
                time_pattern = '%Y-%m-%dT%H:%M:%SZ'
            converted_time = datetime.strptime(value, time_pattern).strftime('%Y-%m-%dT%H%M')
            return converted_time
        except ValueError:
            pass
        raise NotImplementedError(f'cannot format the timestamp {value}')

    @staticmethod
    def _parse_time_range(qualifier, time_range) -> list:
        """
        Converts qualifier timestamp to custom
        return: list of converted custom values
        """
        try:
            compile_timestamp_regex = re.compile(START_STOP_PATTERN)
            converted_timestamp = []
            if qualifier and compile_timestamp_regex.search(qualifier):
                time_range_iterator = compile_timestamp_regex.finditer(qualifier)
                time_range_list = [QueryStringPatternTranslator._format_datetime(each.group())
                                   for each in time_range_iterator]
            else:
                start_time = STOP_TIME - timedelta(minutes=time_range)
                time_range_list = [start_time.strftime('%Y-%m-%dT%H%M'), STOP_TIME.strftime('%Y-%m-%dT%H%M')]
            for timestamp in time_range_list:
                converted_timestamp.append(timestamp)
            return converted_timestamp
        except (KeyError, IndexError, TypeError) as e:
            raise e

    def _get_mapped_field_type(self, mapped_field_array) -> str:
        """
        Returns the type of mapped field array
        :param mapped_field_array: list
        :return: str
        """
        mapped_field = mapped_field_array[0]
        mapped_field_type = "string"
        for key, value in self.config_map.items():
            if mapped_field in value and key in ["int_supported_fields", "timestamp_supported_fields",
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
            if not converted_value.isdigit():
                raise NotImplementedError(f'string type input - {converted_value} is not supported for '
                                          f'integer type fields')
            converted_value = int(value)

        return converted_value

    def _check_value_comparator_support(self, value, comparator, mapped_field_type):
        """
        checks the comparator and value support
        :param value
        :param comparator
        :param mapped_field_type: str
        :return value: str
        """
        operator = self.comparator_lookup[str(comparator)]

        if mapped_field_type != "timestamp" and isinstance(value, str) and \
                comparator in [ComparisonComparators.GreaterThan,
                               ComparisonComparators.GreaterThanOrEqual, ComparisonComparators.LessThan,
                               ComparisonComparators.LessThanOrEqual]:
            raise NotImplementedError(f'{operator.replace(":<", "<").replace(":>", ">")} operator is not supported for '
                                      f'string type input')

        if mapped_field_type == "timestamp" and comparator not in [ComparisonComparators.Like,
                                                                   ComparisonComparators.Matches]:
            value = self._format_datetime(str(value))

        if mapped_field_type == "boolean":
            if comparator not in [ComparisonComparators.Equal, ComparisonComparators.NotEqual,
                                  ComparisonComparators.In]:
                raise NotImplementedError(f'{operator.replace(":<", "<").replace(":>", ">")} '
                                          f'operator is not supported for Boolean type input. '
                                          f'Possible supported operator are [ =, !=, IN, NOT IN ]')

            if not value.lower() in ["true", "false"]:
                raise NotImplementedError('Boolean type field allows only true/false')
        return value

    def _lookup_comparison_operator(self, expression_operator) -> str:
        """
        lookup operators support in gcp chronicle
        :param expression_operator:object
        :return str
        """
        if str(expression_operator) not in self.comparator_lookup:
            raise NotImplementedError(
                f'Comparison operator {expression_operator.name} unsupported for vectra connector')

        return self.comparator_lookup[str(expression_operator)]

    def _eval_comparison_value(self, expression, mapped_field_type):
        """
        Function for parsing comparison expression value
        :param expression: expression object
        :return: formatted expression value
        """
        if (expression.negated or expression.comparator == ComparisonComparators.NotEqual) and \
                mapped_field_type != 'string':
            raise NotImplementedError('Not operator is only supported for string type fields')

        if expression.comparator == ComparisonComparators.Like:
            value = self._format_like(expression.value, mapped_field_type)
        elif expression.comparator == ComparisonComparators.Matches:
            value = self._format_match(expression.value, mapped_field_type)
        elif expression.comparator == ComparisonComparators.In:
            value = self._format_set(expression.value, mapped_field_type, expression)
        elif expression.comparator in [ComparisonComparators.GreaterThan, ComparisonComparators.GreaterThanOrEqual,
                                       ComparisonComparators.LessThan, ComparisonComparators.LessThanOrEqual,
                                       ComparisonComparators.Equal, ComparisonComparators.NotEqual]:
            value = self._format_value_type(expression.value, mapped_field_type)
            value = self._check_value_comparator_support(value, expression.comparator, mapped_field_type)
            value = self._format_equality(value)
        else:
            raise NotImplementedError('Unknown comparator expression operator')
        return value

    def _add_qualifier(self, query, qualifier) -> str:
        """
        Convert the qualifier into epoch time and
        append in the query.
        params: query : str
        params: qualifier
        return: query : str
        """
        time_range = QueryStringPatternTranslator._parse_time_range(qualifier, self.options['time_range'])
        query = f"(({query}) AND (detection.last_timestamp:[{time_range[0]} to {time_range[1]}]))"
        return query

    def _create_parsed_query(self, field_name, value, comparator, is_negated) -> str:
        """
        Creates comparison string for each field_name in mapped_field_array
        :param field_name: str
        :param value
        :param comparator: str
        :param is_negated: boolean
        :return: str
        """
        comparison_string = ""
        if not isinstance(value, list):
            value = [value]
        all_mappings = []
        for values in value:
            if is_negated:
                field_mappings = f'({field_name}:* AND NOT {field_name}{comparator}{values})'
            else:
                field_mappings = f'{field_name}{comparator}{values}'
            all_mappings.append(field_mappings)
        if all_mappings:
            if len(all_mappings) == 1:
                comparison_string += all_mappings[0]
            else:
                condition_string = " OR "
                in_comparison_string = f'{condition_string}'.join(all_mappings)
                comparison_string += in_comparison_string

        return comparison_string

    def _parse_mapped_fields(self, formatted_value, mapped_fields_array, expression) -> str:
        """
        parse mapped fields into boolean expression
        :param formatted_value: str
        :param mapped_fields_array: list
        :param mapped_field_type:str
        :param expression: expression object
        :return: str
        """
        is_negated = None
        comparator = self._lookup_comparison_operator(expression.comparator)
        comparison_string = ""
        comparison_string_new_count = 0
        if expression.negated or expression.comparator == ComparisonComparators.NotEqual:
            is_negated = True
        for field_name in mapped_fields_array:
            comparison_string_new = self._create_parsed_query(field_name, formatted_value, comparator, is_negated)
            if comparison_string_new:
                comparison_string_new_count += 1
                if comparison_string:
                    comparison_string += " OR "
                comparison_string += comparison_string_new

        return comparison_string

    def _eval_combined_comparison_exp(self, expression) -> str:
        """
        Function for parsing combined comparison expression
        :param expression: expression object
        """
        operator = self._lookup_comparison_operator(expression.operator)
        expression_01 = self._parse_expression(expression.expr1)
        expression_02 = self._parse_expression(expression.expr2)
        if not expression_01 or not expression_02:
            return ''
        if isinstance(expression.expr1, CombinedComparisonExpression):
            expression_01 = f'{expression_01}'
        if isinstance(expression.expr2, CombinedComparisonExpression):
            expression_02 = f'{expression_02}'

        query = f'({expression_01}) {operator} ({expression_02})'
        return f'{query}'

    def _eval_combined_observation_exp(self, expression, qualifier=None) -> str:
        """
        Function for parsing combined observation expression
        :param expression: expression object
        :param qualifier: qualifier
        """
        operator = self._lookup_comparison_operator(expression.operator)
        expression_01 = self._parse_expression(expression.expr1, qualifier)
        expression_02 = self._parse_expression(expression.expr2, qualifier)
        query = ''
        if expression_01 and expression_02:
            query = f'({expression_01} {operator} {expression_02})'
        elif expression_01:
            query = f'{expression_01}'
        elif expression_02:
            query = f'{expression_02}'
        return query

    def _parse_expression(self, expression, qualifier=None) -> str:
        """
         Formation of vectra query from ANTLR parsing expression
        :param expression: expression object, ANTLR parsed expression object
        :param qualifier: str, default in None
        :return :None or str
        """
        if isinstance(expression, ComparisonExpression):  # Base Case
            stix_objects = expression.object_path.split(':')
            mapped_fields_array = self.dmm.map_field(stix_objects[0], stix_objects[1])
            mapped_field_type = self._get_mapped_field_type(mapped_fields_array)
            value = self._eval_comparison_value(expression, mapped_field_type)
            query = self._parse_mapped_fields(value, mapped_fields_array, expression)
            return query

        elif isinstance(expression, CombinedComparisonExpression):
            return self._eval_combined_comparison_exp(expression)

        elif isinstance(expression, ObservationExpression):
            query = self._parse_expression(expression.comparison_expression)
            return self._add_qualifier(query, qualifier)

        elif hasattr(expression, 'qualifier') and hasattr(expression, 'observation_expression'):
            if isinstance(expression.observation_expression, CombinedObservationExpression):
                operator = self._lookup_comparison_operator(expression.observation_expression.operator)
                expression_01 = self._parse_expression(expression.observation_expression.expr1, expression.qualifier)
                expression_02 = self._parse_expression(expression.observation_expression.expr2, expression.qualifier)
                query = f'({expression_01} {operator} {expression_02})'
            else:
                query = self._parse_expression(expression.observation_expression, expression.qualifier)
            if qualifier is not None:
                query = self._add_qualifier(query, qualifier)
            return query

        elif isinstance(expression, CombinedObservationExpression):
            return self._eval_combined_observation_exp(expression, qualifier)
        elif isinstance(expression, Pattern):
            return self._parse_expression(expression.expression)
        else:
            raise RuntimeError(f'Unknown Recursion Case for expression={expression}, '
                               f'type(expression)={type(expression)}')

    def parse_expression(self, pattern: Pattern) -> list:
        """
         Formation of vectra query from ANTLR parsing expression.
        :param pattern: expression object, ANTLR parsed expression object
        """
        query = self._parse_expression(pattern)
        vectra_queries = []

        # Query length exceed the max query limit will split the query
        if len(query) > MAX_QUERY_LENGTH:
            obj = QuerySeparator()
            vectra_queries = obj.split_query(query)

        # change single query into list
        if query and not vectra_queries:
            vectra_queries = [query]

        for row in vectra_queries:
            self.qualified_queries.append("query_string=" + row)


def translate_pattern(pattern: Pattern, data_model_mapping, options) -> list:
    """
    Conversion of ANTLR pattern to Vectra query
    :param pattern: expression object, ANTLR parsed expression object
    :param data_model_mapping: DataMapper object, mapping object obtained by parsing json
    :param options: dict, time_range defaults to 5
    :return: list, Vectra queries
    """
    translated_query_strings = QueryStringPatternTranslator(pattern, data_model_mapping, options)
    queries = translated_query_strings.qualified_queries
    return queries


class QuerySeparator:
    """
    split the translated query based on query length
    """

    def split_query(self, query):
        """
        split the query based on query length limit.
        Between two statements if OR is present it will split if AND is present it wont split.
        param query: str
        return queries: list
        """
        try:
            queries = []
            # Based on brackets converting the translated query into nested list
            parsed_query = nestedExpr(opener="(", closer=")", ignoreExpr=White('')).parseString(query).asList()
            parsed_query = parsed_query[0]

            # Check valid parsing
            if len(parsed_query) != 3:
                return [query]

            # process the each statement its need to split as separate query or not
            statement_1 = self.split_sub_query(parsed_query[0])
            statement_2 = self.split_sub_query(parsed_query[2])
            operator = parsed_query[1]

            if str(statement_1).count('Unable to split') or str(statement_2).count('Unable to split'):
                return [query]

            # statement is greater than query length limit and it was split.
            if isinstance(statement_1, list) or isinstance(statement_2, list):

                # Try to combine the split query
                statement_1 = self.combine_list_query(statement_1)
                statement_2 = self.combine_list_query(statement_2)

                # AND operator is processed if only its contains timestamp then will attach the timestamp in each query
                queries = self.attach_timestamp(statement_1, statement_2, operator)

                if str(queries).count('Unable to split'):
                    return [query]

            # statements are lesser than query length limit and it wont split.
            elif statement_1 and statement_2:
                combined_statement = statement_1 + ' ' + operator + ' ' + statement_2
                if len(combined_statement) > MAX_QUERY_LENGTH:
                    if operator == 'AND':
                        queries.append(query)
                    else:
                        queries.append(statement_1)
                        queries.append(statement_2)
                else:
                    queries.append(combined_statement)
            else:
                queries.append(query)

            return queries
        except Exception as e:
            logger.info(f'Unable to split the query. Error occurred {str(e)}')
            return [query]

    def split_sub_query(self, parsed_query):
        """
        Iterate the query from list and based on operator separate the query or combine the query.
        param query: str
        return queries: list or str
        """

        # iterate other than IN operator
        if len(parsed_query) == 3:
            statement_1 = parsed_query[0]
            statement_2 = parsed_query[2]
            operator = parsed_query[1]
            queries = []
            query_list = [statement_1, statement_2]
            for index, statement in enumerate(query_list, start=0):
                if any(isinstance(i, list) for i in statement):
                    statement = self.split_sub_query(statement)
                elif isinstance(statement, list):
                    statement = ' '.join(map(str, statement))
                if statement and len(statement) > MAX_QUERY_LENGTH:
                    statement = self.split_query_and_or_operator(statement)

                if index == 0:
                    statement_1 = statement
                else:
                    statement_2 = statement

            if isinstance(statement_1, list) or isinstance(statement_2, list):
                queries = self.attach_timestamp(statement_1, statement_2, operator)
                return queries

            combined_query = '(' + statement_1 + ') ' + operator + ' (' + statement_2 + ')'

            if len(combined_query) > MAX_QUERY_LENGTH:
                if operator == 'AND':
                    return 'Unable to split'
                queries.append(statement_1)
                queries.append(statement_2)
                return queries
            return combined_query
        elif any(isinstance(i, list) for i in parsed_query):
            # iterate for IN operator
            return self.handle_translated_in_operator(parsed_query)
        elif isinstance(parsed_query, list):
            combined_query = '(' + ' '.join(map(str, parsed_query)) + ')'
            if len(combined_query) > MAX_QUERY_LENGTH:
                combined_query = self.split_query_and_or_operator(combined_query)
            return combined_query
        else:
            return '(' + parsed_query + ')'

    @staticmethod
    def split_query_and_or_operator(parsed_query, query_len=MAX_QUERY_LENGTH):
        """ Split the query based on AND/OR operator.
        param query: str, MAX_QUERY_LENGTH: int
        return queries: list or str """
        start = 0
        index = 0
        result = []
        combined_query = ''

        while index < len(parsed_query):
            if 'OR' in parsed_query[index:len(parsed_query)]:
                index = parsed_query[index:len(parsed_query)].index('OR')
                index = start + index + 2
            elif 'AND' in parsed_query[index:len(parsed_query)]:
                index = parsed_query[index:len(parsed_query)].index('AND')
                index = start + index + 3
            else:
                index = len(parsed_query)
                if len(combined_query + parsed_query[start: index]) > query_len:
                    if combined_query:
                        result.append('(' + combined_query.rstrip('OR').rstrip('AND') + ')')
                    if parsed_query[start: index]:
                        result.append('(' + parsed_query[start: index].lstrip('(').rstrip(')') + ')')
                else:
                    combined_query += parsed_query[start: index]
                    combined_query = combined_query.lstrip('(').rstrip(')')
                    result.append('(' + combined_query + ')')
                break
            if len(combined_query + parsed_query[start: index]) > query_len and combined_query:
                query = combined_query.rstrip('OR').rstrip('AND')
                query = query.lstrip('(').rstrip(')').rstrip("'").rstrip(",")
                if query:
                    result.append('(' + query + ')')
                combined_query = ''
            combined_query += parsed_query[start: index]
            start = index
        return result

    @staticmethod
    def combine_list_query(query_list):
        """ Combine the query from list.
        param query: list, return queries: list """

        query = ''
        queries = []

        # exit the process for invalid arguments
        if isinstance(query_list, str) or len(query_list) == 1:
            return query_list

        for index, each_query in enumerate(query_list, start=0):
            if not query:
                query = each_query
                continue

            combined_query = query + ' OR ' + each_query
            if len(combined_query) > MAX_QUERY_LENGTH:
                queries.append(query)
                query = each_query
                if len(query_list) - 1 == index:
                    queries.append(query)
                continue

            query = combined_query

            if len(query_list) - 1 == index:
                queries.append(query)
                continue

        return queries

    @staticmethod
    def attach_timestamp(statement_1, statement_2, operator):
        """Attach the timestamp in query"""
        queries = []

        if operator == 'AND':
            if statement_2.count('detection.last_timestamp')==1\
                    and len(statement_2) < TIMESTAMP_LENGTH:
                if not (statement_2.count('(') and statement_2.count(')')):
                    statement_2 = '(' + statement_2 + ')'
                if ') to (' in statement_2:
                    statement_2 = statement_2.replace(') to (', ' to ')
                queries = ['(' + row + ') AND ' + statement_2 for row in statement_1]
            else:
                return 'Unable to split'

        if operator == 'OR':
            queries += statement_1 if isinstance(statement_1, list) else [statement_1]
            queries += statement_2 if isinstance(statement_2, list) else [statement_2]

        return queries

    def handle_translated_in_operator(self, parsed_query):
        """ Process the translated query having IN operator in STIX pattern.
        Params Query: List, return Query: List """
        query = ''
        queries = []
        for row in parsed_query:
            if isinstance(row, str):
                query += row
            elif isinstance(row, list):

                combined_query = '(' + ' '.join(map(str, row)) + ')'

                if combined_query.count('NOT') and any(isinstance(i, list) for i in row):
                    combined_query = self.split_sub_query(row)

                query = query.lstrip('OR').lstrip('AND')

                if isinstance(combined_query, list):
                    queries += [query + value for value in combined_query]
                elif isinstance(combined_query, str) and len(combined_query) > MAX_QUERY_LENGTH:
                    separated = self.split_query_and_or_operator(combined_query, MAX_QUERY_LENGTH - len(query))
                    queries += [query + value for value in separated]
                else:
                    queries += [query + combined_query]
                query = ''
        return queries
