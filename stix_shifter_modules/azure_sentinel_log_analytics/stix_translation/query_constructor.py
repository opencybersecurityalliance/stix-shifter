from stix_shifter_utils.stix_translation.src.patterns.pattern_objects import ObservationExpression, \
    ComparisonExpression, ComparisonExpressionOperators, ComparisonComparators, Pattern, CombinedComparisonExpression, \
    CombinedObservationExpression
from stix_shifter_utils.stix_translation.src.patterns.errors import SearchFeatureNotSupportedError
from datetime import datetime, timedelta
import re

START_STOP_PATTERN = r"(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?Z)"


class QueryStringPatternTranslator:
    COUNTER = 0

    # comparator lookup for implementing negation operator
    negated_comparator_lookup = {
        ComparisonComparators.GreaterThan: "le",
        ComparisonComparators.GreaterThanOrEqual: "lt",
        ComparisonComparators.LessThan: "ge",
        ComparisonComparators.LessThanOrEqual: "gt",
        ComparisonComparators.Equal: "ne",
        ComparisonComparators.NotEqual: "eq",
        ComparisonComparators.In: "ne"
    }

    def __init__(self, pattern: Pattern, data_model_mapper, time_range):
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
            format_list.append('\'{}\''.format(item))
        return format_list

    @staticmethod
    def _format_match(value) -> str:
        """
         Formatting value in the event of MATCHES operation
         encapsulating the value inside regex keyword
         :param value: str
         :return: str
         """
        return '\'{}\''.format(value)

    @staticmethod
    def _format_equality(value) -> str:
        """
          Formatting value in the event of equality operation
          :param value: str
          :return: str
          """
        return '\'{}\''.format(value)

    @staticmethod
    def _format_like(value) -> str:
        """
        Formatting value in the event of LIKE operation
        :param value: str
        :return: str
        """
        return '\'{}\''.format(value)

    @staticmethod
    def _escape_value(value) -> str:
        """
        Formats and replaces backslashes and single quoted parenthesis
        :param value: str
        :return: str
        """
        if isinstance(value, str):
            return '{}'.format(value.replace('\\', '\\\\').replace('\"', '\\"').replace('(', '\\(').replace(')', '\\)'))
        else:
            return value

    @staticmethod
    def _format_value_without_quotes(value):
        """
        Formats and replaces values with escape character into value without quotes
        :param value: str
        :return: str
        """
        values = []
        if isinstance(value, list):
            for each in value:
                values.append('{}'.format(each.replace('\'', '')))
            value = values
        else:
            value = value.replace('\'', '')
        return value

    @staticmethod
    def _format_value_to_lower_case(value):
        """
        Formats and replaces values with escape character into value without quotes
        :param value: str
        :return: str
        """
        values = []
        if isinstance(value, list):
            for each in value:
                values.append('{}'.format(each).lower())
            value = values
        else:
            value = value.lower()
        return value

    @staticmethod
    def _parse_mapped_fields(self, expression, value, comparator, stix_field, mapped_fields_array, counter):
        """
        Mapping the stix object property with their corresponding property in sentinel odata query
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

        def format_comparision_string(comparison_string, mapped_field, lambda_func):
            # check for mapped_field that has '.' character -> example [fileStates.name,processes.name]
            if '.' in mapped_field:
                collection_attribute_array = mapped_field.split('.')
                collection_name = collection_attribute_array[0]
                attribute_nested_level = '/'.join(collection_attribute_array[1:])

                attribute_expression = '({fn}/'.format(fn=lambda_func) + attribute_nested_level + ')'
                # ip address in data source is like "sourceAddress": "IP: 92.63.194.101 [2]\r"
                # to get ip address from data source using contains keyword ODATA query
                if comparator == 'contains':
                    comparison_string += " and {collection_name}/any({fn}:{comparator}({attribute_expression}, " \
                                            "{value})))".format(collection_name=collection_name, fn=lambda_func,
                                                                attribute_expression=attribute_expression,
                                                                comparator=comparator, value=value)
                else:
                    comparison_string += " and {collection_name}/any({fn}:{attribute_expression} {comparator} " \
                                            "{value}))".format(collection_name=collection_name, fn=lambda_func,
                                                            attribute_expression=attribute_expression,
                                                            comparator=comparator,
                                                            value=value)
            else:
                # check for mapped field that does not have '.' character -> example [azureTenantId,title]
                if comparator == 'contains':
                    comparison_string += "{comparator}{mapped_field}, {value}".format(
                        mapped_field=mapped_field, comparator=comparator, value=value)
                else:
                    comparison_string += "{mapped_field} {comparator} {value}".format(
                        mapped_field=mapped_field, comparator=comparator, value=value)
            return comparison_string

        # loop for custom logic to form IN operator related query
        for mapped_field in mapped_fields_array:
            lambda_func = 'query' + str(counter)

            # for In operator, loop the format comparision string for each values in the list.
            if expression.comparator == ComparisonComparators.In:
                if isinstance(values, list):
                    values_count = len(values)
                    for value in values:
                        comparison_string = format_comparision_string(comparison_string, mapped_field, lambda_func)
                        if values_count > 1:
                            if expression.negated:
                                comparison_string += " and "
                            else:
                                comparison_string += " or "
                            values_count -= 1
            # to form queries other than IN operator
            else:
                comparison_string = format_comparision_string(comparison_string, mapped_field, lambda_func)

            if mapped_fields_count > 1:
                if expression.negated:
                    comparison_string += " and "
                else:
                    comparison_string += " or "
                mapped_fields_count -= 1
        return comparison_string

    def _lookup_comparison_operator(self, expression_operator):
        if str(expression_operator) not in self.comparator_lookup:
            raise NotImplementedError(
                "Comparison operator {} unsupported for Azure Sentinel adapter".format(expression_operator.name))
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
                time_range_list = [each.group() for each in time_range_iterator]
            else:
                stop_time = datetime.utcnow()
                start_time = stop_time - timedelta(hours=24)
                converted_starttime = start_time.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
                converted_stoptime = stop_time.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
                time_range_list = [converted_starttime, converted_stoptime]

            value = ('{mapped_field} between (datetime({start_time}) .. datetime({stop_time}))'
                        ).format(mapped_field=mapped_field, start_time=time_range_list[0],
                                stop_time=time_range_list[1])
            format_string = '{value}'.format(value=value)
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
            # should be (x, y, z, ...)
            elif expression.comparator == ComparisonComparators.In:
                value = self._format_set(expression.value)
            elif expression.comparator == ComparisonComparators.Equal \
                    or expression.comparator == ComparisonComparators.NotEqual \
                    or expression.comparator == ComparisonComparators.GreaterThan \
                    or expression.comparator == ComparisonComparators.LessThan \
                    or expression.comparator == ComparisonComparators.GreaterThanOrEqual \
                    or expression.comparator == ComparisonComparators.LessThanOrEqual:
                # Should be in single-quotes
                value = self._format_equality(expression.value)
            # '%' -> '*' wildcard, '_' -> '?' single wildcard
            elif expression.comparator == ComparisonComparators.Like:
                value = self._format_like(expression.value)
            else:
                value = self._escape_value(expression.value)

            if expression.negated:
                if expression.comparator in [ComparisonComparators.Like, ComparisonComparators.Matches]:
                    raise SearchFeatureNotSupportedError("'NOT' Operator is not supported for LIKE and MATCHES")
                elif stix_object in ['ipv4-addr', 'ipv6-addr'] or stix_field in ['src_ref.value', 'dst_ref.value']:
                    raise SearchFeatureNotSupportedError("'NOT' Operator is not supported for IPV4 or IPV6 address")
                comparator = self.negated_comparator_lookup.get(expression.comparator)

            # to remove single quotes in specific field value
            if stix_field in ['pid', 'parent_ref.pid', 'account_last_login']:
                if expression.comparator in [ComparisonComparators.Like, ComparisonComparators.Matches]:
                    raise SearchFeatureNotSupportedError('"{operator}" operator is not supported for '
                                                         '"{stix_field}" attribute'
                                                         .format(operator=expression.comparator.name.upper(),
                                                                 stix_field=stix_field))
                value = self._format_value_without_quotes(value)

            # COUNTER is used to form sequential lambda function names for OData4 queries per comparison observation
            ''' eg. processes/any(query1:contains(tolower(query1/path), 'c:\\windows\\system32')) and 
            processes/any(query2:contains(tolower(query2/name), 'exe')) '''
            self.COUNTER += 1

            comparison_string = self._parse_mapped_fields(self, expression, value, comparator, stix_field,
                                                          mapped_fields_array, self.COUNTER)

            if len(mapped_fields_array) > 1:
                # More than one data source field maps to the STIX attribute, so group comparisons together.
                grouped_comparison_string = "(" + comparison_string + ")"
                comparison_string = grouped_comparison_string

            return "{}".format(comparison_string)

        elif isinstance(expression, CombinedComparisonExpression):
            operator = self._lookup_comparison_operator(expression.operator)
            expression_01 = self._parse_expression(expression.expr1)
            expression_02 = self._parse_expression(expression.expr2)
            if not expression_01 or not expression_02:
                return ''
            if isinstance(expression.expr1, CombinedComparisonExpression):
                expression_01 = "({})".format(expression_01)
            if isinstance(expression.expr2, CombinedComparisonExpression):
                expression_02 = "({})".format(expression_02)
            query_string = "{} {} {}".format(expression_01, operator, expression_02)
            return "{}".format(query_string)
        elif isinstance(expression, ObservationExpression):
            parse_string = self._parse_expression(expression.comparison_expression)
            time_string = self._parse_time_range(qualifier, self._time_range)
            sentinel_query = "({}) and ({})".format(parse_string, time_string)
            self.final_query_list.append(sentinel_query)
        elif hasattr(expression, 'qualifier') and hasattr(expression, 'observation_expression'):
            if isinstance(expression.observation_expression, CombinedObservationExpression):
                self._parse_expression(expression.observation_expression.expr1, expression.qualifier)
                self._parse_expression(expression.observation_expression.expr2, expression.qualifier)
            else:
                parse_string = self._parse_expression(expression.observation_expression.comparison_expression,
                                                      expression.qualifier)
                time_string = self._parse_time_range(expression.qualifier, self._time_range)
                sentinel_query = "({}) and ({})".format(parse_string, time_string)
                self.final_query_list.append(sentinel_query)
        elif isinstance(expression, CombinedObservationExpression):
            self._parse_expression(expression.expr1, qualifier)
            self._parse_expression(expression.expr2, qualifier)
        elif isinstance(expression, Pattern):
            return "{expr}".format(expr=self._parse_expression(expression.expression))
        else:
            raise RuntimeError("Unknown Recursion Case for expression={}, type(expression)={}".format(
                expression, type(expression)))

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
    translated_query = dialect_name + ' |' + " where " + ','.join(query.final_query_list)
    return translated_query
