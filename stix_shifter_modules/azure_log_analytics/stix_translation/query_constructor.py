from stix_shifter_utils.stix_translation.src.patterns.pattern_objects import ObservationExpression, \
    ComparisonExpression, ComparisonComparators, Pattern, CombinedComparisonExpression, \
    CombinedObservationExpression
from datetime import datetime, timedelta
import re
from os import path
import logging
import json
from stix_shifter_modules.azure_log_analytics.stix_translation.transformers import HexToInteger


START_STOP_PATTERN = r"(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?Z)"
CONFIG_MAP_PATH = "json/config_map.json"
logger = logging.getLogger(__name__)


class FileNotFoundException(Exception):
    pass


class QueryStringPatternTranslator:

    def __init__(self, pattern: Pattern, data_model_mapper, time_range):
        logger.info("Azure Log Analytics")
        self.config_map = self.load_json(CONFIG_MAP_PATH)
        self.dmm = data_model_mapper
        self.comparator_lookup = self.dmm.map_comparator()
        self._time_range = time_range
        self.pattern = pattern

        # List of queries for each observation
        self.final_query_list = []
        # Translated query string without any qualifiers
        self.translated = self.parse_expression(pattern)

    @staticmethod
    def _format_set(value) -> list:
        """
        Formatting list of values in the event of IN operation
        :param value: str
        :return: list
        """
        value_list = value.values
        format_list = []
        for item in value_list:
            format_list.append(f'\'{QueryStringPatternTranslator._escape_value(item)}\'')
        return format_list

    @staticmethod
    def _format_match(value) -> str:
        """
         Formatting value in the event of MATCHES operation
         encapsulating the value inside regex keyword
         :param value: str
         :return: str
         """
        if not re.search(r'[()}\]\[{*^$+?|]', value):
            value = value.replace('\\', '\\\\')
        return f"'{value}'"

    @staticmethod
    def _format_equality(value) -> str:
        """
          Formatting value in the event of equality operation
          :param value: str
          :return: str
          """
        return f'\'{value}\''

    @staticmethod
    def _format_like(value) -> str:
        """
        Formatting value in the event of LIKE operation
        :param value: str
        :return: str
        """
        return f'\'{value}\''

    @staticmethod
    def _escape_value(value) -> str:
        """
        Formats and replaces backslashes and single quoted parenthesis
        :param value: str
        :return: str
        """
        if isinstance(value, str):
            return '{}'.format(value.replace('\\', '\\\\').replace('\"', '\\"'))
        return value

    @staticmethod
    def load_json(rel_path_of_file):
        """ Consumes a json file and returns a dictionary
        :param rel_path_of_file: str
        :return: dict """
        _json_path = path.dirname(path.abspath(__file__)) + "/" + rel_path_of_file
        try:
            if path.exists(_json_path):
                with open(_json_path, encoding='utf-8') as f_obj:
                    config = json.load(f_obj)
                    config = json.dumps(config).replace('Entities.', 'parsed_entities.')
                    return json.loads(config)
            raise FileNotFoundException
        except FileNotFoundException as e:
            raise FileNotFoundError(f'{rel_path_of_file} not found') from e

    @staticmethod
    def _negate_comparison(comparison_string, mapped_fields_array, comparator):
        """ Add negate operator in comparison string
        :param comparison_string: str
        :param mapped_fields_array: list
        :param comparator: str
        :return: str """
        not_null_expression = ""

        if comparator != ComparisonComparators.NotEqual:
            comparison_string = f"not ({comparison_string})"

        for index, field in enumerate(mapped_fields_array):
            if 'Entities' in field or 'ExtendedProperties' in field:
                field = field.replace('Entities', 'parsed_entities').replace('ExtendedProperties', 'parsed_properties')
                if index == 0:
                    logical_operator = ""
                else:
                    logical_operator = " and "
                not_null_expression += logical_operator + f"notnull({field})"

        if not_null_expression:
            comparison_string = f"{not_null_expression} and {comparison_string}"

        return comparison_string

    @staticmethod
    def _format_file_hash(stix_field, comparison_string):
        """ Formatting the file hash
        :param stix_field, comparison_string: str
        :return comparison_string: str """
        file_hash = stix_field.replace("hashes.", "").replace("'", "").replace("-", "")
        file_statement = f"parsed_entities.Algorithm == '{file_hash}' and "
        comparison_string = f"({file_statement}{comparison_string})"
        return comparison_string

    def _convert_enum_values(self, value, mapped_field, comparator):
        """ Convert enum values
          :param value: str
          :param mapped_field: str
          :param comparator: str
          :return: str """
        if comparator not in [ComparisonComparators.Equal, ComparisonComparators.NotEqual, ComparisonComparators.In]:
            raise NotImplementedError(f'{comparator.name} operator is not supported for Enum type input. Possible '
                                      f'supported operator are [ =, !=, IN, NOT IN ]')

        if "Severity" in mapped_field:
            mapped_field = "Severity"

        conversion_json = self.config_map['enum_supported_values'].get(mapped_field, {})

        if isinstance(value, list):
            converted_list = []
            for row in value:
                row = row.replace("\'", "")
                if row in conversion_json:
                    conversion_value = conversion_json[row]
                    converted_list.append(f"\'{conversion_value}\'")
                else:
                    raise NotImplementedError(f'Unsupported ENUM values provided. Possible supported'
                                              f' enum values are {list(conversion_json.keys())}')
            return converted_list

        elif value.replace("\'", "") in conversion_json:
            conversion_value = conversion_json[value.replace("\'", "")]
            value = f'\'{conversion_value}\''
            return value

        raise NotImplementedError(f'Unsupported ENUM values provided. Possible supported'
                                  f' enum values are {list(conversion_json.keys())}')

    @staticmethod
    def _convert_score_values(value, comparator):
        """ Convert 0-100 into 0-1
          :param value: str or list
          :param comparator: str
          :return: str or list"""
        if isinstance(value, list):
            for index, row in enumerate(value):
                if row.replace("\'", "").isdigit():
                    conversion_value = float(row.replace("\'", "")) / 10
                    value[index] = f'\'{conversion_value}\''
        else:
            if str(value).replace("\'", "").isdigit():
                conversion_value = float(str(value).replace("\'", "")) / 10
                if comparator in [ComparisonComparators.Like, ComparisonComparators.Matches]:
                    value = f'\'{conversion_value}\''
                else:
                    value = conversion_value
        return value

    @staticmethod
    def _check_int_values(value):
        """ check the input value contains valid integer
        :param value
        :return formatted value """
        if isinstance(value, list):
            for index, row in enumerate(value):
                if row.replace("\'", "").isdigit():
                    conversion_value = int(str(row).replace("\'", ""))
                    value[index] = f'\'{conversion_value}\''
                else:
                    raise NotImplementedError(f'string type input - {row} is not supported for'
                                              f' integer type fields')
        else:
            if str(value).replace("\'", "").isdigit():
                conversion_value = int(str(value).replace("\'", ""))
                value = conversion_value
            else:
                raise NotImplementedError(f'string type input - {value} is not supported for '
                                          f'integer type fields')
        return value

    def _parse_mapped_fields(self, expression, value, comparator, mapped_fields_array):
        """
        Mapping the stix object property with their corresponding property in azure log analytics data query
        from_stix_map.json will be used for mapping
        :param expression: expression object, ANTLR parsed expression object
        :param value: str
        :param comparator: str
        :param mapped_fields_array: list, Mapping available in from_stix_map.json
        :return: str, whose part of the odata query for each value
        """
        comparison_string = ""
        values = value
        mapped_fields_count = len(mapped_fields_array)

        # loop for custom logic to form IN operator related query
        for mapped_field in mapped_fields_array:

            # security alert Entities field mapped to parsed_entities field
            if 'Entities.' in mapped_field:
                mapped_field = mapped_field.replace('Entities', 'parsed_entities')

            # security alert ExtendedProperties field mapped to parsed_entities field
            if 'ExtendedProperties.' in mapped_field:
                mapped_field = mapped_field.replace('ExtendedProperties', 'parsed_properties')

            # hexadecimal values conversion
            if mapped_field in self.config_map['hexadecimal_fields']:
                if expression.comparator in [ComparisonComparators.Like, ComparisonComparators.Matches,
                                             ComparisonComparators.In]:
                    raise NotImplementedError(f'IN/LIKE/MATCHES operator is unsupported for hexadecimal fields in'
                                              f' AZURE LOG ANALYTICS')
                conversion_value = HexToInteger.transform(str(value).replace("\'", ""))
                value = f'\'{conversion_value}\''

            # enum values conversion
            if mapped_field in self.config_map['enum_supported_fields']:
                value = self._convert_enum_values(value, mapped_field, expression.comparator)

            # check integer supported values
            if mapped_field in self.config_map['int_supported_fields'] and \
                    expression.comparator not in [ComparisonComparators.Like, ComparisonComparators.Matches]:
                value = self._check_int_values(value)

            # score values conversion
            if mapped_field in self.config_map['score_fields']:
                value = self._convert_score_values(value, expression.comparator)

            # for In operator, loop the format comparison string for each values in the list.
            if expression.comparator == ComparisonComparators.In:
                if isinstance(values, list):
                    comparison_string += f"{mapped_field} {comparator} ({', '.join(value)})"
            # to form queries other than IN operator
            else:
                if expression.comparator in [ComparisonComparators.Like, ComparisonComparators.Matches]:
                    if mapped_field in self.config_map['int_supported_fields'] + \
                            self.config_map['timestamp_supported_fields']:
                        mapped_field = f"tostring({mapped_field})"

                comparison_string += f"{mapped_field} {comparator} {value}"

            if mapped_fields_count > 1:
                if expression.negated or expression.comparator == ComparisonComparators.NotEqual:
                    comparison_string += " and "
                else:
                    comparison_string += " or "
                mapped_fields_count -= 1
        return comparison_string

    def _lookup_comparison_operator(self, expression_operator):
        if str(expression_operator) not in self.comparator_lookup:
            raise NotImplementedError(
                f"Comparison operator {expression_operator.name} unsupported for AZURE LOG ANALYTICS")
        return self.comparator_lookup[str(expression_operator)]

    @staticmethod
    def _parse_time_range(qualifier, time_range):
        """
        :param qualifier: str, input time range i.e START t'2019-04-10T08:43:10.003Z' STOP t'2019-04-20T10:43:10.003Z'
        :param time_range: int, value available from main.py in options variable
        :return: str, format_string bound with time range provided
        """
        try:
            compile_timestamp_regex = re.compile(START_STOP_PATTERN)
            mapped_field = "TimeGenerated"
            if qualifier and compile_timestamp_regex.search(qualifier):
                time_range_iterator = compile_timestamp_regex.finditer(qualifier)
                time_range_list = []
                for each in time_range_iterator:
                    date_time = each.group()
                    if re.search(r"\d{4}(-\d{2}){2}T\d{2}(:\d{2}){2}Z", str(date_time)):  # without milli seconds
                        date_time = datetime.strptime(each.group(), '%Y-%m-%dT%H:%M:%SZ'). \
                                        strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
                    time_range_list.append(date_time)
            else:
                stop_time = datetime.utcnow()
                start_time = stop_time - timedelta(hours=24)
                converted_starttime = start_time.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
                converted_stoptime = stop_time.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
                time_range_list = [converted_starttime, converted_stoptime]

            value = f'{mapped_field} between (datetime({time_range_list[0]}) .. datetime({time_range_list[1]}))'
            format_string = f'{value}'
            return format_string
        except (KeyError, IndexError, TypeError) as e:
            raise e

    def _parse_expression(self, expression, qualifier=None) -> str:
        """
           Complete formation of native query from ANTLR expression object
           :param expression: expression object, ANTLR parsed expression object
           :param qualifier: str | None
           :return: None or native query as the method call is recursive
           """
        if isinstance(expression, ComparisonExpression):  # Base Case
            # Resolve STIX Object Path to a field in the target Data Model
            stix_object, stix_field = expression.object_path.split(':')
            # Multiple data source fields may map to the same STIX Object
            mapped_fields_array = self.dmm.map_field(stix_object, stix_field)
            # Resolve the comparison symbol to use in the query string (usually just ':')
            comparator = self._lookup_comparison_operator(expression.comparator)

            # Some values are formatted differently based on how they're being compared
            if expression.comparator == ComparisonComparators.Matches:  # needs forward slashes
                value = self._format_match(expression.value)
                value = self._escape_value(value)
            # should be (x, y, z, ...)
            elif expression.comparator == ComparisonComparators.In:
                value = self._format_set(expression.value)
            elif expression.comparator in [ComparisonComparators.Equal, ComparisonComparators.NotEqual]:
                # Should be in single-quotes
                value = self._format_equality(expression.value)
                value = self._escape_value(value)
            elif expression.comparator in [ComparisonComparators.GreaterThan, ComparisonComparators.GreaterThanOrEqual,
                                           ComparisonComparators.LessThan,
                                           ComparisonComparators.LessThanOrEqual]:
                for mapped_field in mapped_fields_array:
                    if mapped_field.replace('Entities', 'parsed_entities') not in \
                            self.config_map['int_supported_fields']:
                        raise NotImplementedError(f"Comparison operator {comparator} unsupported for AZURE LOG "
                                                  f"ANALYTICS attribute {mapped_field}")
                value = expression.value

            # '%' -> '*' wildcard, '_' -> '?' single wildcard
            elif expression.comparator == ComparisonComparators.Like:
                value = self._format_like(expression.value)
                value = self._escape_value(value)
            else:
                value = self._escape_value(expression.value)

            comparison_string = self._parse_mapped_fields(expression, value, comparator, mapped_fields_array)

            if len(mapped_fields_array) > 1:
                # More than one data source field maps to the STIX attribute, so group comparisons together.
                grouped_comparison_string = "(" + comparison_string + ")"
                comparison_string = grouped_comparison_string

            if expression.negated or expression.comparator == ComparisonComparators.NotEqual:
                comparison_string = self._negate_comparison(comparison_string, mapped_fields_array,
                                                            expression.comparator)

            # security alert file hash conversion
            if 'parsed_entities' in comparison_string:
                if stix_field in self.config_map["file_hash_fields"]:
                    comparison_string = self._format_file_hash(stix_field, comparison_string)

            return f"{comparison_string}"

        elif isinstance(expression, CombinedComparisonExpression):
            operator = self._lookup_comparison_operator(expression.operator)
            expression_01 = self._parse_expression(expression.expr1)
            expression_02 = self._parse_expression(expression.expr2)
            if not expression_01 or not expression_02:
                return ''
            if isinstance(expression.expr1, CombinedComparisonExpression):
                expression_01 = f"({expression_01})"
            if isinstance(expression.expr2, CombinedComparisonExpression):
                expression_02 = f"({expression_02})"
            query_string = f"{expression_01} {operator} {expression_02}"
            return f"{query_string}"
        elif isinstance(expression, ObservationExpression):
            parse_string = self._parse_expression(expression.comparison_expression)
            time_string = self._parse_time_range(qualifier, self._time_range)
            sentinel_query = f"({parse_string}) and ({time_string})"
            self.final_query_list.append(sentinel_query)
        elif hasattr(expression, 'qualifier') and hasattr(expression, 'observation_expression'):
            if isinstance(expression.observation_expression, CombinedObservationExpression):
                self._parse_expression(expression.observation_expression.expr1, expression.qualifier)
                self._parse_expression(expression.observation_expression.expr2, expression.qualifier)
            else:
                parse_string = self._parse_expression(expression.observation_expression.comparison_expression,
                                                      expression.qualifier)
                time_string = self._parse_time_range(expression.qualifier, self._time_range)
                sentinel_query = f"({parse_string}) and ({time_string})"
                self.final_query_list.append(sentinel_query)
        elif isinstance(expression, CombinedObservationExpression):
            self._parse_expression(expression.expr1, qualifier)
            self._parse_expression(expression.expr2, qualifier)
        elif isinstance(expression, Pattern):
            return f"{self._parse_expression(expression.expression)}"
        else:
            raise RuntimeError(f"Unknown Recursion Case for expression={expression}, "
                               f"type(expression)={type(expression)}")

    def parse_expression(self, pattern: Pattern):
        """
          parse_expression --> Native query
          :param pattern: expression object, ANTLR parsed expression object
          :return:str, Odata filter query(native query)
          """
        return self._parse_expression(pattern)


def translate_pattern(pattern: Pattern, data_model_mapping, options):
    """
    Conversion of expression object to translated query
    :param pattern: expression object, ANTLR parsed expression object
    :param data_model_mapping: DataMapper object, mapping object obtained by parsing from_stix_map.json
    :param options: dict, contains 2 keys result_limit defaults to 10000, time_range defaults to 5
    :return: str, translated query
    """
    dialect_name = data_model_mapping.dialect
    # Query result limit and time range can be passed into the QueryStringPatternTranslator if supported by the DS
    time_range = options['time_range']
    query = QueryStringPatternTranslator(pattern, data_model_mapping, time_range)
    query = ' or '.join(query.final_query_list)

    # parsing and expanding the Entities, ExtendedProperties fields for security alert query
    expand_query_fields = ""
    if 'parsed_entities' in query:
        expand_query_fields = "| mv-expand parsed_entities = parse_json(Entities) "
    if 'parsed_properties' in query:
        expand_query_fields += "| mv-expand parsed_properties = parse_json(ExtendedProperties) "

    if expand_query_fields:
        translated_query = f"{dialect_name} {expand_query_fields}" \
                           f"| where {query} | summarize arg_max(TimeGenerated, *) by TimeGenerated, SystemAlertId"
    else:
        translated_query = dialect_name + ' |' + " where " + query
    return translated_query
