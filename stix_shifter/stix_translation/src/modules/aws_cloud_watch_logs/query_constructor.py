from stix_shifter.stix_translation.src.patterns.pattern_objects import ObservationExpression, ComparisonExpression, \
    ComparisonExpressionOperators, ComparisonComparators, Pattern, \
    CombinedComparisonExpression, CombinedObservationExpression, ObservationOperators, StartStopQualifier
from stix_shifter.stix_translation.src.utils.transformers import TimestampToMilliseconds
from datetime import datetime, timedelta
import os.path as path
import json
import re

PROTOCOL_LOOKUP_JSON_FILE = 'json/network_protocol_map.json'
MASTER_CONFIG_FILE = 'json/master_config.json'
TIMESTAMP_PATTERN = r"\d{4}(-\d{2}){2}T\d{2}(:\d{2}){2}(\.\d+)?Z"


class QueryStringPatternTranslator:
    # Change comparator values to match with supported data source operators
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
        ComparisonComparators.Matches: 'LIKE',
        ComparisonComparators.IsSubSet: '',
        # ComparisonComparators.IsSuperSet: '',
        ObservationOperators.Or: 'OR',
        ObservationOperators.And: 'OR'
    }
    aws_query = "fields {fields}{stix_filter} {parse_filter}{logtype_filter} | filter ({filter_query})"

    def __init__(self, pattern: Pattern, data_model_mapper, time_range, from_stix_json_filename):
        self.dmm = data_model_mapper
        self.pattern = pattern
        self._time_range = time_range
        self.json_file = from_stix_json_filename
        self.log_type = self.load_json('json/' + path.basename(from_stix_json_filename)).get('log-type')
        self._log_config_data = self.load_json(MASTER_CONFIG_FILE)
        self._protocol_lookup_needed = True if self.log_type in ['vpcflow'] else False
        self._parse_statement = []
        self.qualified_queries = []
        self.time_range_lst = []
        self._parse_filter = ''
        self._parse_statement = {}
        self.logtype_filter = self._log_config_data[self.log_type].get('logtype_filter')
        self.translated = self.parse_expression(pattern)

    def build_parse_statement(self, parse_statement):
        """
        Parse statements for guardduty logs
        :param parse_statement: dict, from master config json file
        :return: None
        """
        if self.log_type == 'guardduty':
            validate = []
            self._parse_statement = []
            for key, value in parse_statement.items():
                filter_string = " or strlen ({validate}) > 0".format(validate=key)
                validate.append(filter_string)
                parse_str = value.split(' ')[1]
                if not parse_str.startswith('/'):
                    parse_string = " | parse {parse} as {field}".format(parse=value, field=key)
                    self._parse_statement.append(parse_string)
                else:
                    parse_string = " | parse {parse}".format(parse=value)
                    self._parse_statement.append(parse_string)
            self._parse_filter = "source = 'aws.guardduty'" + ''.join(validate)

    def protocol_lookup(self, value):
        """
        Function for protocol number lookup
        :param value:str
        :return:str if log type is vpcflow, list if log type is guardduty
        """
        protocol_value = []
        value = value.values if hasattr(value, 'values') else value
        protocol_json = self.load_json(PROTOCOL_LOOKUP_JSON_FILE)
        if self._protocol_lookup_needed:
            if isinstance(value, list):
                protocol_value = [protocol_json.get(each_value.lower()) for each_value in value if each_value.lower() in
                                  protocol_json]
            else:
                protocol_value = protocol_json.get(value.lower())
        else:
            if isinstance(value, list):
                protocol_value = list(map(str.upper, value))
                existing_protocol_lower = list(map(str.lower, value))
                for index, v in enumerate(existing_protocol_lower):
                    protocol_value.insert(2*index+1, v)
            else:
                protocol_value.extend([value.lower(), value.upper()])
        return protocol_value

    @staticmethod
    def load_json(rel_path_of_file):
        """
        Consumes a json file and returns a dictionary
        :param rel_path_of_file: str, path of json file
        :return: dictionary
        """
        _json_path = path.abspath(path.join(path.join(__file__, ".."), rel_path_of_file))
        if path.exists(_json_path):
            with open(_json_path) as f_obj:
                return json.load(f_obj)
        else:
            raise FileNotFoundError

    @staticmethod
    def _format_set(values) -> str:
        """
        Formatting list of values in the event of IN operation
        :param values: str
        :return: list
        """
        values = values.values if hasattr(values, 'values') else values
        return list(map("{}".format, values))

    @staticmethod
    def _format_matches(value) -> str:
        """
        Formatting value in the event of MATCHES operation
        encapsulating the value inside regex keyword
        :param value: str
        :return: str
        """
        return '/{}/'.format(value) if not isinstance(value, list) else ['/{}/'.format(each) for each in value]

    @staticmethod
    def _format_equality(comparator, value) -> str:
        """
        Formatting value in the event of equality operation
        :param value: str
        :return: str
        """
        if comparator == '=' and not isinstance(value, list):
            comparator = '=~'
            return "/^(?i){}$/".format(value), comparator
        return "'{}'".format(value) if not isinstance(value, list) else value, comparator

    @staticmethod
    def _format_like(value) -> str:
        """
        Formatting value in the event of LIKE operation
        :param value: str
        :return: str
        """
        # Replacing value with % to .* and _ to . for supporting Like comparator
        if not isinstance(value, list):
            compile_regex = re.compile(r'.*(\%|\_).*')
            if compile_regex.match(value):
                value = '/(?i){}$/'.format(value.replace('%', '.*').replace('_', '.'))
            else:
                value = '/(?i){}/'.format(value)
        return value

    @staticmethod
    def _format_datetime(value, field) -> str:
        """
        Formating value in the event of value is datetime
        :param value: datetime value
        :return: list, timestamp in milliseconds or timestamp itself
        """
        values = []
        if field == 'updated_at':
            compile_timestamp_regex = re.compile(TIMESTAMP_PATTERN)
            val = value.values if hasattr(value, 'values') else [value]
            for value in val:
                temp = compile_timestamp_regex.search(value)
                if temp:
                    values.append(temp.group(0))
                else:
                    raise ValueError("invalid timestamp in Stix field 'updatedAt'")
        else:
            transformer = TimestampToMilliseconds()
            values = value.values if hasattr(value, 'values') else [value]
            milli_secs_lst = list(map(transformer.transform, values))
            values = list(map(lambda x: '{}'.format(str(x)[:-3]), milli_secs_lst))
        return values

    @staticmethod
    def _negate_comparison(comparison_string):
        return "NOT ({})".format(comparison_string)

    def _parse_mapped_fields(self, expression, value, comparator, mapped_fields_array):
        """
        Mapping the stix object property with their corresponding property, from stix logtype json will be used for
        mapping
        :param expression: expression object, ANTLR parsed expression object
        :param value: str
        :param comparator: str
        :param mapped_fields_array: list, attributes in from stix logtype json file
        :return: str, filter condition will be constructed
        """
        comparison_string = ""
        mapped_fields_count = len(mapped_fields_array)
        for mapped_field in mapped_fields_array:
            if expression.comparator == ComparisonComparators.In:
                comparison_string += '{mapped_field} {comparator} {value}'.format(mapped_field=mapped_field,
                                                                                  comparator=comparator, value=value)
            elif expression.comparator == ComparisonComparators.IsSubSet:
                comparison_string += 'isIpv4InSubnet({mapped_field},{value})'.format(mapped_field=mapped_field,
                                                                                     value=value)

            else:
                if isinstance(value, list):
                    comparison_string += "({})".format(' OR '.join(map(lambda x: "{mapped_field} {comparator}"
                                                                                 " '{value}'".
                                                                       format(mapped_field=mapped_field,
                                                                              comparator=comparator,
                                                                              value=x), value)))
                else:
                    comparison_string += "{mapped_field} {comparator} {value}".format(mapped_field=mapped_field,
                                                                                      comparator=comparator,
                                                                                      value=value)
            if 'parse_attributes' in self._log_config_data.get(self.log_type):
                if mapped_field in self._log_config_data.get(self.log_type).get('parse_attributes').keys():
                    parse_attributes_from_config = self._log_config_data.get(self.log_type).get('parse_attributes').get(
                        mapped_field).get('parse_string')
                    parse_value = parse_attributes_from_config
                    self._parse_statement.update({mapped_field: parse_value})

            if mapped_fields_count > 1:
                comparison_string += " OR "
                mapped_fields_count -= 1
        return comparison_string

    def _parse_time_range(self, qualifier, time_range):
        """
        Format the input time range UTC timestamp to Unix time
        :param time_range: int, value available from main.py in options variable
        :return: str, format_string
        """
        format_string = ''
        try:
            compile_timestamp_regex = re.compile(TIMESTAMP_PATTERN)
            transformer = TimestampToMilliseconds()
            if qualifier and compile_timestamp_regex.search(qualifier):
                time_range_iterator = map(lambda x: int(transformer.transform(x.group())/1000),
                                          compile_timestamp_regex.finditer(qualifier))
            # Default time range Start time = Now - 5 minutes and Stop time  = Now
            else:
                stop_time = datetime.now()
                start_time = int(round((stop_time - timedelta(minutes=time_range)).timestamp()))
                stop_time = int(round(stop_time.timestamp()))
                time_range_iterator = [start_time, stop_time]
            self.time_range_lst.append([each for each in time_range_iterator])
            return format_string
        except (KeyError, IndexError, TypeError) as e:
            raise e

    @staticmethod
    def _lookup_comparison_operator(self, expression_operator):
        if expression_operator not in self.comparator_lookup:
            raise NotImplementedError("Comparison operator {} unsupported for "
                                      "AWS cloudwatch logs adapter".format(expression_operator.name))
        return self.comparator_lookup[expression_operator]

    def _parse_expression(self, expression, qualifier=None) -> str:
        """
        Complete formation of AWS query from ANTLR expression object
        :param expression: expression object, ANTLR parsed expression object
        :param qualifier: str, default in None
        :return: str, comparison string
        """
        if isinstance(expression, ComparisonExpression):  # Base Case
            # Resolve STIX Object Path to a field in the target Data Model
            stix_object, stix_field = expression.object_path.split(':')
            # Custom condition for protocol lookup if log type == 'vpcflow'
            if stix_field.lower() == 'protocols[*]':
                existing_protocol_value = expression.value
                value = self.protocol_lookup(expression.value)
                if (not value) or (isinstance(value, list) and None in value):
                    raise NotImplementedError("Un-supported protocol '{}' for operation '{}' for aws '{}' logs".format(
                        expression.value, expression.comparator, path.basename(self.log_type)))
                expression.value = self._format_set(value) if isinstance(value, list) and not\
                    self._protocol_lookup_needed and expression.comparator not in [ComparisonComparators.Matches,
                                                                                   ComparisonComparators.In]\
                    else value
            mapped_fields_array = self.dmm.map_field_json(stix_object, stix_field, path.basename(self.json_file))
            comparator = self._lookup_comparison_operator(self, expression.comparator)
            comparison_string = self.__eval_comparison_value(comparator, expression, mapped_fields_array, stix_field)
            # Reverting back the protocol value in expression to existing
            if stix_field.lower() == 'protocols[*]':
                expression.value = existing_protocol_value
            if len(mapped_fields_array) > 1:
                # More than one data source field maps to the STIX attribute, so group comparisons together.
                grouped_comparison_string = "(" + comparison_string + ")"
                comparison_string = grouped_comparison_string

            if expression.negated:
                if comparison_string:
                    comparison_string = self._negate_comparison(comparison_string)
            return "{}".format(comparison_string)

        elif isinstance(expression, CombinedComparisonExpression):
            operator = self._lookup_comparison_operator(self, expression.operator)
            expression_01 = self._parse_expression(expression.expr1)
            expression_02 = self._parse_expression(expression.expr2)
            if not expression_01 or not expression_02:
                query_string = ""
            else:
                query_string = "({}) {} ({})".format(expression_01, operator, expression_02)
            return query_string
        elif isinstance(expression, ObservationExpression):
            filter_query = self._parse_expression(expression.comparison_expression, qualifier)
            if filter_query:
                self._parse_time_range(qualifier, self._time_range)
                self.build_parse_statement(self._parse_statement)
                self.qualified_queries.append(self.aws_query.format(fields=', '.join(self._log_config_data
                                                                                     .get(self.log_type)
                                                                                     .get('display_fields')),
                                                                    filter_query=filter_query,
                                                                    stix_filter=''.join(self._parse_statement) if
                                                                    self._parse_statement else '',
                                                                    parse_filter='| filter ' + self._parse_filter if
                                                                    self._parse_filter else '',
                                                                    logtype_filter='| filter ' + self.logtype_filter
                                                                    if self.logtype_filter else ''))
                # Re-initialize parse statement for multiple observation
                self._parse_statement = {}
            return None
        elif isinstance(expression, CombinedObservationExpression):
            self._parse_expression(expression.expr1, qualifier)
            self._parse_expression(expression.expr2, qualifier)
            return None
        elif isinstance(expression, StartStopQualifier):
            if hasattr(expression, 'observation_expression'):
                return self._parse_expression(getattr(expression, 'observation_expression'), expression.qualifier)
        elif isinstance(expression, Pattern):
            return "{expr}".format(expr=self._parse_expression(expression.expression))
        else:
            raise RuntimeError("Unknown Recursion Case for expression={}, type(expression)={}".format(
                expression, type(expression)))

    def __eval_comparison_value(self, comparator, expression, mapped_fields_array, stix_field):
        """
        Function for parsing comparison expression value
        :param comparator: str, comparator value
        :param expression: expression object, ANTLR parsed expression object
        :param mapped_fields_array: list, values available in from stix logtype json file
        :param stix_field: str, stix field
        :return: str, comparison string
        """
        if stix_field in ["start", "end", "updated_at"]:
            if expression.comparator not in [ComparisonComparators.Matches, ComparisonComparators.Like]:
                value = self._format_datetime(expression.value, stix_field)
            else:
                raise NotImplementedError("STIX field '{}' un-supported for LIKE and MATCHES operation".format(
                    stix_field))
        elif expression.comparator == ComparisonComparators.Matches:
            value = self._format_matches(expression.value)
        elif expression.comparator == ComparisonComparators.In:
            value = self._format_set(expression.value)
        elif expression.comparator == ComparisonComparators.Equal or \
                expression.comparator == ComparisonComparators.NotEqual:
            value, comparator = self._format_equality(comparator, expression.value)
        elif expression.comparator == ComparisonComparators.Like:
            value = self._format_like(expression.value)
        else:
            value = '"{}"'.format(expression.value)
        comparison_string = self._parse_mapped_fields(expression, value, comparator, mapped_fields_array)
        return comparison_string

    def parse_expression(self, pattern: Pattern):
        return self._parse_expression(pattern)


def translate_pattern(pattern: Pattern, data_model_mapping, options):
    """
    Conversion of expression object to AWS query
    :param pattern: expression object, ANTLR parsed expression object
    :param data_model_mapping: DataMapper object, mapping object obtained by parsing json
    :param options: dict, timerange defaults to 5
    :return: str, AWS query
    """
    timerange = options['timerange']
    final_queries = []
    for each_json_file in data_model_mapping.from_stix_files_cnt:
        queries_obj = QueryStringPatternTranslator(pattern, data_model_mapping, timerange, each_json_file)
        qualifier_list = list(zip(*queries_obj.time_range_lst))
        queries_string = queries_obj.qualified_queries
        for index, each_query in enumerate(queries_string, start=0):
            translate_query_dict = dict()
            translate_query_dict['logType'] = queries_obj.log_type
            translate_query_dict['limit'] = 1000
            translate_query_dict['queryString'] = each_query
            translate_query_dict['startTime'] = qualifier_list[0][index]
            translate_query_dict['endTime'] = qualifier_list[1][index]
            translate_query_dict = json.dumps(translate_query_dict)
            final_queries.append(translate_query_dict)
    return final_queries
