from stix_shifter_utils.stix_translation.src.patterns.pattern_objects import ObservationExpression, ComparisonExpression, \
    ComparisonExpressionOperators, ComparisonComparators, Pattern, \
    CombinedComparisonExpression, CombinedObservationExpression, ObservationOperators, StartStopQualifier
import json
import os.path as path
from stix_shifter_utils.stix_translation.src.utils.transformers import TimestampToUTC
from stix_shifter_utils.stix_translation.src.json_to_stix import observable
from datetime import datetime, timedelta
from functools import reduce
import operator as op
import re

FILE = "file"
SEARCH_FOLDER = 'folder'
PROCESS = 'process'
SOCKET = "socket"
NETWORK = "network"
ADAPTER = "adapter"
DEFAULT_SEARCH_FOLDER = '(system folder; folders of system folder)'
RELEVANCE_PROPERTY_MAP_JSON = "json/relevance_property_format_string_map.json"
START_STOP_PATTERN = r"\d{4}(-\d{2}){2}T\d{2}(:\d{2}){2}(\.\d+)?Z"
WHOSE_STRING = "whose ({})"
USER_OF_PROCESS = "user"


class RelevanceQueryStringPatternTranslator:
    """
    Stix to Native query translation
    """
    comparator_lookup = {
        ComparisonExpressionOperators.And: "AND",
        ComparisonExpressionOperators.Or: "OR",
        ComparisonComparators.Equal: "=",
        ComparisonComparators.NotEqual: "!=",
        ComparisonComparators.Like: "contains",
        ComparisonComparators.Matches: "matches",
        ComparisonComparators.GreaterThan: "is greater than",
        ComparisonComparators.GreaterThanOrEqual: "is greater than or equal to",
        ComparisonComparators.LessThan: "is less than",
        ComparisonComparators.LessThanOrEqual: "is less than or equal to",
        ComparisonComparators.In: "=",
        ObservationOperators.Or: 'OR',
        # Treat AND's as OR's -- Unsure how two ObsExps wouldn't cancel each other out.
        ObservationOperators.And: 'OR'
    }
    _stix_object_format_string_lookup_dict = {
        FILE: '''("file", name of it | "n/a",
                    "sha256", sha256 of it | "n/a",
                    "sha1", sha1 of it | "n/a",
                    "md5", md5 of it | "n/a",
                    pathname of it | "n/a",
                    size of it | 0,
                    (modification time of it - "01 Jan 1970 00:00:00 +0000" as time)/second) of files {}''',
        PROCESS: '''("process", name of it | "n/a",
                    pid of it as string | "n/a",
                    "sha256", sha256 of image file of it | "n/a",
                    "sha1", sha1 of image file of it | "n/a",
                    "md5", md5 of image file of it | "n/a",
                    pathname of image file of it | "n/a",
                    ppid of it as string | "n/a",
                    (if (windows of operating system) then
                    user of it as string | "n/a"
                    else name of user of it as string | "n/a"),
                    size of image file of it | 0,
                    (if (windows of operating system) then
                    (creation time of it | "01 Jan 1970 00:00:00 +0000" as time -
                    "01 Jan 1970 00:00:00 +0000" as time)/second  else
                    (start time of it | "01 Jan 1970 00:00:00 +0000" as time -
                    "01 Jan 1970 00:00:00 +0000" as time)/second))
                    of processes {}''',
        SOCKET: '''("Local Address", local address of it as string | "n/a",
                    "Remote Address", remote address of it as string | "n/a",
                    "Local port", local port of it | -1,
                    "remote port", remote port of it | -1,
                    "Process name", names of processes of it,
                    pid of process of it as string | "n/a",
                    "sha256", sha256 of image files of processes of it | "n/a",
                    "sha1", sha1 of image files of processes of it | "n/a",
                    "md5", md5 of image files of processes of it | "n/a",
                    pathname of image files of processes of it | "n/a",
                    ppid of process of it as string | "n/a",
                    (if (windows of operating system) then
                    user of processes of it as string | "n/a"
                    else name of user of processes of it as string | "n/a"),
                    size of image files of processes of it | 0,
                    (if (windows of operating system) then
                    (creation time of process of it | "01 Jan 1970 00:00:00 +0000" as time -
                    "01 Jan 1970 00:00:00 +0000" as time)/second else
                    (start time of process of it | "01 Jan 1970 00:00:00 +0000" as time -
                    "01 Jan 1970 00:00:00 +0000" as time)/second),
                    "TCP", tcp of it, "UDP", udp of it)
                    of sockets {}''',
        ADAPTER: '''("Address", address of it as string | "n/a",
                    mac address of it as string | "n/a") of adapters {}'''
        }

    def __init__(self, pattern: Pattern, data_model_mapper, time_range):
        self.dmm = data_model_mapper
        self.pattern = pattern
        self._time_range = time_range
        self.qualified_queries = []
        self.qualifier_string = ''
        self.search_folder = DEFAULT_SEARCH_FOLDER
        self._master_obj = None
        self._split_master_obj_list = []
        self._relevance_string_list = []
        self._relevance_query_for_split_attr = []
        self._relevance_property_format_string_dict = self.load_json(RELEVANCE_PROPERTY_MAP_JSON)
        self._time_range_comparator_list = [self._lookup_comparison_operator(each) for each in
                                            (ComparisonComparators.GreaterThanOrEqual,
                                             ComparisonComparators.LessThanOrEqual)]
        self.parse_expression(pattern)

    @staticmethod
    def load_json(rel_path_of_file):
        """
        Consumes the relevance property format string mapping json and returns a dictionary
        :param rel_path_of_file: str, path of relevance property format string mapping json file
        :return: dictionary
        """
        relevance_json_path = path.abspath(path.join(path.join(__file__, ".."), rel_path_of_file))
        if path.exists(relevance_json_path):
            with open(relevance_json_path) as f_obj:
                return json.load(f_obj)
        else:
            raise FileNotFoundError

    @staticmethod
    def _format_equality(value) -> str:
        """
        Formatting value in the event of equality operation
        :param value: str
        :return: str
        """
        return '"{}"'.format(value)

    @staticmethod
    def _format_set(values) -> str:
        """
        Formatting list of values in the event of IN operation
        :param values: str
        :return: list
        """
        return list(map('"{}"'.format, values))

    @staticmethod
    def _format_like(value) -> str:
        """
        Formatting value in the event of LIKE operation
        :param value: str
        :return: str
        """
        # Replacing value with % to .* and _ to . for supporting Like comparator
        compile_regex = re.compile(r'.*(\%|\_).*')
        if compile_regex.match(value):
            value = 'regex"({}$)"'.format(value.replace('%', '.*').replace('_', '.'))
        else:
            value = '"{}"'.format(value)
        return value

    @staticmethod
    def _format_matches(value) -> str:
        """
        Formatting value in the event of MATCHES operation
        encapsulating the value inside regex keyword
        :param value: str
        :return: str
        """
        return 'regex"({})"'.format(value)

    @staticmethod
    def _negate_comparison(comparison_string, comparator):
        """
        Function for adding Negation operator to relevance query
        :param comparison_string: str
        :param comparator: str
        :return: str
        """
        if comparator.lower() != 'matches' and comparison_string:
            comparison_string = "NOT ({})".format(comparison_string)
        return comparison_string

    def _lookup_comparison_operator(self, expression_operator):
        """
        Comparison operator lookup with error handling for un-supported operators
        :param expression_operator: str
        :return: str
        """
        if expression_operator not in self.comparator_lookup:
            raise NotImplementedError(
                "Comparison operator {} unsupported for BigFix adapter".format(expression_operator.name))
        return self.comparator_lookup.get(expression_operator)

    @staticmethod
    def _html_encoding_escape_character(value) -> str:
        """
        Function for html encoding of special characters
        For e.g. &#92; is the ascii equivalent of r'\'(backslash)
        We are converting all inbound \\(double backslash) with r'\'(backslash) so as to escape character
        having special meaning
        :param value: str
        :return: str
        """
        master_encoding_dict = {'\\': '&#92;'}
        if hasattr(value, 'values') and isinstance(value.values, list):
            value = [str(each).replace(key, encode_str) for each in value.element_iterator()
                     for key, encode_str in master_encoding_dict.items()]
        else:
            for key, encode_str in master_encoding_dict.items():
                value = str(value).replace(key, encode_str)
        return value

    @staticmethod
    def _check_value_type(value):
        """
        Function returning the type of value i.e mac, ipv4, ipv6
        :param value: str
        :return: list
        """
        value = list(map(str, value)) if isinstance(value, list) else [str(value)]
        value_type = []
        non_combinable_values_attr = ['mac']
        combinable_value_attr = ['ipv4', 'ipv6']
        for each in value:
            for key, pattern in observable.REGEX.items():
                if key not in ('date', 'ipv4_cidr', 'domain_name') and bool(re.search(pattern, each)):
                    if value_type and key not in value_type:
                        if not reduce(op.and_, [each in combinable_value_attr for each in value_type]) or \
                                key in non_combinable_values_attr:
                            raise ValueError("Cannot combine {} with {} for IN operation".format(key, value_type))
                    else:
                        value_type.append(key)
                        break
        return value_type

    @staticmethod
    def _map_transformer_to_field(value, comparator) -> str:
        """
        Function for mapping transformer to field based on inbound value
        i.e. name of process as string = "process.exe" as string
        as string  ==> transformer
        :param value: str
        :param comparator: str
        :return: tuple
        """
        _transformer_hierarchy = ['', 'as lowercase', 'as string']
        if isinstance(value, list):
            value = [each.replace('"', '') if each.replace('"', '').isdigit() else each for each in list(value)]
            transformer = _transformer_hierarchy[max([_transformer_hierarchy.index('as lowercase')
                                                      if each.replace('"', '').isalpha() else
                                                      _transformer_hierarchy.index('') if
                                                      each.replace('"', '').isdigit() else
                                                      _transformer_hierarchy.index('as string') for each in value])]
        else:
            value = value.replace('"', '') if value.replace('"', '').isdigit() and comparator != 'contains' else value
            transformer = 'as lowercase' if value.replace('"', '').isalpha() else '' if \
                value[0].replace('"', '').isdigit() else 'as string'
            if comparator == 'contains':
                transformer = 'as string'
        return value, transformer

    @staticmethod
    def _query_const_from_list_subroutine(expr_list):
        """
        A sub method for _query_construction_from_list method in aiding query construction
        :param expr_list: list, relevance query list
        :return: str
        """
        interim_list = []
        interim_str = None
        for index, each_exp_list in enumerate(expr_list):
            for each_exp in each_exp_list:
                interim_list.append(each_exp)
            if index == len(expr_list) - 1:
                interim_str = '({})'.format(' OR '.join(interim_list))
        return interim_str

    def _query_construction_from_list(self, value, comparison_string_list, conditional_attr):
        """
        Function to group and form the relevance query
        :param value: str
        :param comparison_string_list: list, list of relevance field and keyword
        :param conditional_attr: str, Conditional Flag for mapping to if-then-else structure
        or query formation with comparator(AND/OR)
        :return:
        """
        comparison_string = ""
        condition_based_map_dict = {
            'user': "(if (windows of operating system) then {} else {})"
        }
        master_qry_list = []
        if comparison_string_list:
            if conditional_attr:
                if isinstance(value, list):
                    for each_value_list in comparison_string_list:
                        interim_str = self._query_const_from_list_subroutine(each_value_list)
                        master_qry_list.append(interim_str)
                    comparison_string = condition_based_map_dict.get(conditional_attr).format(*master_qry_list)
                else:
                    interim_qry_str = self._query_const_from_list_subroutine(comparison_string_list)
                    comparison_string = condition_based_map_dict.get(conditional_attr).format(
                        *interim_qry_str.strip('()').split(' OR '))
            else:
                if isinstance(value, list):
                    for each_in_value_list in zip(*comparison_string_list):
                        interim_qry_str = self._query_const_from_list_subroutine(each_in_value_list)
                        master_qry_list.append(interim_qry_str)
                    comparison_string = '({})'.format(' OR '.join(master_qry_list))
                else:
                    comparison_string = self._query_const_from_list_subroutine(comparison_string_list)
        return comparison_string

    def _relevance_qry_list_phrasing(self, value, comparator, mapped_field, is_negate):
        """
        A sub method for _parse_mapped_field method in aiding query construction
        :param value: str
        :param comparator: str
        :param mapped_field: str
        :param is_negate: boolean
        :return: list
        """
        operator_mapping = {"default": "format_string_generic", "matches": "format_string_match"}
        comparison_string_list = [] if isinstance(value, str) else [[] for _ in value]
        mapped_field = "{} of ".format(mapped_field) if self._relevance_string_list else mapped_field
        mapped_field_relevance_string = "{} {} of it".format(mapped_field, ' of '.join(
            self._relevance_string_list)).lstrip()
        format_string_key = operator_mapping.get(comparator) if comparator in operator_mapping \
            else operator_mapping.get('default')
        value, transformer = self._map_transformer_to_field(value, comparator)
        if isinstance(value, str):
            transformer_field, transformer_value = (transformer, '') \
                if (value.startswith('regex') and comparator == 'contains') \
                else (transformer, transformer)
            comparison_string_list.append('{} {}'.format('NOT' if comparator.lower() == 'matches' and is_negate
                                                         else '', self._relevance_property_format_string_dict.
                                                         get('format_string').get(format_string_key)
                                                         .format(mapped_field=mapped_field_relevance_string,
                                                                 transformer_field=transformer_field,
                                                                 comparator=comparator, value=value,
                                                                 transformer_value=transformer_value)).strip())
        # Case of handling IN operation
        else:
            for index, each_value in enumerate(value):
                comparison_string_list[index].append(self._relevance_property_format_string_dict
                                                     .get('format_string').get(format_string_key)
                                                     .format(mapped_field=mapped_field_relevance_string,
                                                             transformer_field=transformer,
                                                             comparator=comparator, value=each_value,
                                                             transformer_value=transformer))
        return comparison_string_list

    def get_master_obj_of_obs_exp(self, expression, objects_list):
        """
        Function to parse observation expression and return a single master object(i.e file, process, socket) involved
        The logic of this function is
            - Observation expression is de-capsulated until a single comparison expression is available
            - Object of current comparison exp is parsed i.e (file:name ==> file)
            - master_obj is initialized to the least object in hierarchy structure ( i.e file)
            - if current_obj's (file) index in object_list > master_obj
                then master_obj is replaced with current_obj
        :param expression: expression object, ANTLR parsed expression object
        :param objects_list: list, List of cyber observable objects i.e ['file', 'process', 'socket']
        :return: None
        """
        regex_val_marked_for_expr_split = ['mac']
        object_marked_for_expr_split = ['mac-addr:value', 'network-traffic:src_ref.value']
        if hasattr(expression, 'object_path'):
            stix_object, stix_field = expression.object_path.split(':')
            value = expression.value.values if hasattr(expression.value, 'values') else expression.value
            value_type = self._check_value_type(value)
            is_value_type_mac = reduce(op.and_, [each_value in regex_val_marked_for_expr_split
                                                 for each_value in value_type]) if value_type else False
            mapped_field = self.dmm.map_field(stix_object, stix_field)[0]
            current_comparison_obj = mapped_field.split('.')[0]
            if current_comparison_obj in self._relevance_property_format_string_dict.get('object_hierarchy'):
                if is_value_type_mac and expression.object_path in object_marked_for_expr_split:
                    self._split_master_obj_list.append(ADAPTER)
                else:
                    if not self._master_obj or objects_list.index(current_comparison_obj) > \
                            objects_list.index(self._master_obj):
                        self._master_obj = current_comparison_obj
            else:
                if expression.object_path in object_marked_for_expr_split:
                    self._split_master_obj_list.append(ADAPTER)
        else:
            self.get_master_obj_of_obs_exp(expression.expr1, objects_list)
            self.get_master_obj_of_obs_exp(expression.expr2, objects_list)

    @staticmethod
    def _parse_time_range(qualifier, stix_obj, relevance_map_dict, time_range, range_operator_list):
        """
        Format the input time range
        i.e <START|STOP>t'2019-04-20T10:43:10.003Z to %d %b %Y %H:%M:%S %z"(i.e 23 Oct 2018 12:20:14 +0000)
        :param qualifier: str | None, input time range i.e START t'2019-04-10T08:43:10.003Z'
        STOP t'2019-04-20T10:43:10.003Z'
        :param stix_obj: str, file or process stix object
        :param relevance_map_dict: dict, relevance property format string
        :param time_range: int, value available from main.py in options variable
        :return: str, format_string bound with time range provided
        """
        format_string = ''
        format_string_list = []
        epoch_time_string = "01 Jan 1970 00:00:00 +0000"
        qualifier_master_dict = {
            FILE:
                {
                    "mapped_field": ["modification time"],
                    "extra_mapped_string": "",
                    "transformer": "as time",
                    "format_pattern": "format_string_range",
                    "add_timestamp_to_relevance": 1,
                    "default_if_attr_undefined": '',
                    "os_dependency": 0
                },
            PROCESS:
                {
                    "mapped_field": ["creation time", "start time"],
                    "extra_mapped_string": "",
                    "transformer": "as time",
                    "format_pattern": "format_string_range",
                    "add_timestamp_to_relevance": 1,
                    "default_if_attr_undefined": '| "{}"'.format(epoch_time_string),
                    "os_dependency": 1
                },
            SOCKET:
                {
                    "mapped_field": ["creation time", "start time"],
                    "extra_mapped_string": " of process",
                    "transformer": "as time",
                    "format_pattern": "format_string_range",
                    "add_timestamp_to_relevance": 1,
                    "default_if_attr_undefined": '| "{}"'.format(epoch_time_string),
                    "os_dependency": 1
                },
            ADAPTER:
                {
                    "add_timestamp_to_relevance": 0,
                }}
        condition_format_for_time = """(if (windows of operating system) then {time_exp1} else {time_exp2})"""
        qualifier_keys_list = ['mapped_field', 'extra_mapped_string', 'transformer', 'default_if_attr_undefined']
        try:
            if qualifier_master_dict.get(stix_obj).get('add_timestamp_to_relevance'):
                compile_timestamp_regex = re.compile(START_STOP_PATTERN)
                transformer = TimestampToUTC()
                mapped_field, extra_mapped_string, str_transformer, default_if_attr_undefined = \
                    [qualifier_master_dict.get(stix_obj).get(each_key) for each_key in qualifier_keys_list]
                if qualifier and compile_timestamp_regex.search(qualifier):
                    time_range_iterator = map(lambda x: transformer.transform(x.group()),
                                              compile_timestamp_regex.finditer(qualifier))
                # Default time range Start time = Now - 5 minutes and Stop time  = Now
                else:
                    stop_time = datetime.now()
                    start_time = stop_time - timedelta(minutes=time_range)
                    time_range_iterator = map(lambda x: transformer.transform(x, is_default=True),
                                              [start_time, stop_time])
                time_range_tuple = [each for each in time_range_iterator]
                for each in mapped_field:
                    interim_format_string_list = []
                    for index_op, each_operator in enumerate(range_operator_list):
                        interim_format_string_list.append(relevance_map_dict.get('format_string').
                                                          get(qualifier_master_dict.get(stix_obj).get('format_pattern'))
                                                          .format(mapped_field=each,
                                                                  extra_mapped_string=extra_mapped_string,
                                                                  default_if_attr_undefined=default_if_attr_undefined,
                                                                  default_value_transformer=str_transformer if
                                                                  default_if_attr_undefined else '',
                                                                  comparator=each_operator, start_value='"{}"'.
                                                                  format(time_range_tuple[index_op]),
                                                                  transformer=str_transformer))
                    format_string_list.append('({})'.format(' AND '.join(interim_format_string_list)))
                if qualifier_master_dict.get(stix_obj).get('os_dependency'):
                    format_string = condition_format_for_time.format(time_exp1=format_string_list[0],
                                                                     time_exp2=format_string_list[1])
                else:
                    format_string = ' '.join(format_string_list)
            return format_string
        except (KeyError, IndexError, TypeError) as e:
            raise e

    def get_field_relevance_qry(self, current_obj, master_obj):
        """
        A recursive function for traversing and forming relevance query of current comparison expression
        with reference to master object of observation expression.
        The mapping references are available in relevance_property_format_string.json
        :param current_obj: object of current comparison expression
        :param master_obj: master object of observation expression as returned by get_master_obj_of_obs_exp method
        :return: list, A list of relevance query keywords
        """
        if current_obj in self._relevance_property_format_string_dict.get('object_hierarchy'):
            if current_obj != master_obj:
                try:
                    parent_obj_references_dict = self._relevance_property_format_string_dict.get('object_hierarchy').\
                        get(master_obj).get('reference')
                except AttributeError:
                    # The exception catch is in the event of mac address value given with network-traffic:src-ref
                    master_obj = 'socket'
                    parent_obj_references_dict = self._relevance_property_format_string_dict.get('object_hierarchy'). \
                        get(master_obj).get('reference')
                if parent_obj_references_dict:
                    for each_key in parent_obj_references_dict:
                        self._relevance_string_list.insert(0, parent_obj_references_dict.get(each_key))
                        if current_obj == each_key:
                            break
                        else:
                            self.get_field_relevance_qry(current_obj, each_key)

    def _parse_mapped_fields(self, value, comparator, mapped_fields_array, *args):
        """
        Mapping the stix object property with their corresponding property in relevance query
        from_stix_map.json will be used for mapping
        :param value: str
        :param comparator: str
        :param mapped_fields_array: list, Mapping available in from_stix_map.json
        :param args: tuple
        conditional_attr: str, A flag for conditional relevance qry formation
        eg. user attribute of process is OS specific,
        is_negate: boolean, A flag to check if negation of expression needed
        :return: str, whose part of the relevance query for each value
        """
        comparison_string_list = []
        conditional_attr, is_negate = args
        for mapped_field in mapped_fields_array:
            mapped_field = mapped_field.split('.')[-1]
            if mapped_field.lower() != SEARCH_FOLDER:
                comparison_string_list.append(self._relevance_qry_list_phrasing(value, comparator, mapped_field,
                                                                                is_negate))
        comparison_string = self._query_construction_from_list(value, comparison_string_list, conditional_attr)
        return comparison_string

    @staticmethod
    def clean_format_string(format_string):
        """
        Formats and replaces carriage return(\r), newline character(\n), spaces > 2, tab with 1 space
        :param format_string: str
        :return: str
        """
        return re.sub(r'\r|\n|\s{2,}|\t', ' ', format_string)

    def _is_exp_split_needed(self, expression):
        """
        Function to parse comparison expression and return True if query needs to split into individual API queries
        i.e. In the event of mac address and ipv4 value given within same observation expression
        Both the attributes have to be split into 2 API queries(No common parent object)
        :param expression: expression object, ANTLR parsed expression object
        :return: tuple
        """
        attr_for_non_expr_modification = 'mac-addr:value'
        attr_marked_for_expr_split = [attr_for_non_expr_modification, 'network-traffic:src_ref.value']
        object_marked_for_expr_split = ['mac']
        other_objects_for_non_split_like_mac = ['ipv4', 'ipv6']
        is_split_expr = False
        is_expr_modified = False
        if hasattr(expression, 'object_path'):
            value = expression.value.values if hasattr(expression.value, 'values') else expression.value
            value_type = self._check_value_type(value)
            stix_obj_attr = expression.object_path
            is_value_type_mac = reduce(op.and_, [each_value in object_marked_for_expr_split
                                                 for each_value in value_type]) if value_type else False
            is_value_type_ipv4_ipv6 = reduce(op.and_, [each_value in other_objects_for_non_split_like_mac
                                                       for each_value in value_type]) if value_type else False
            if stix_obj_attr in attr_marked_for_expr_split:
                if value_type:
                    if is_value_type_mac:
                        is_split_expr = True
                        if stix_obj_attr != attr_for_non_expr_modification:
                            is_expr_modified = True
                            expression.object_path = attr_for_non_expr_modification
                    # Below elif for network-traffic:src-ref with ipv4 and ipv6 values
                    elif is_value_type_ipv4_ipv6:
                        if stix_obj_attr == attr_for_non_expr_modification:
                            raise ValueError("Irrelevant value:{} for attribute {}. Please check from_stix pattern".
                                             format(value, stix_obj_attr))
                # Below elif for STIX pattern with mac address, network-traffic:src_ref LIKE, matches operation
                else:
                    if stix_obj_attr == attr_for_non_expr_modification:
                        is_split_expr = True
        else:
            self._is_exp_split_needed(expression.expr1)
            self._is_exp_split_needed(expression.expr2)
        return is_split_expr, is_expr_modified

    def _parse_expression(self, expression, qualifier=None):
        """
        Complete formation of relevance query from ANTLR expression object
        :param expression: expression object, ANTLR parsed expression object
        :param qualifier: str | None
        :return: None or relevance query as the method call is recursive
        """
        if isinstance(expression, ComparisonExpression):  # Base Case
            return self.__eval_comparison_exp(expression)
        elif isinstance(expression, CombinedComparisonExpression):
            operator = self._lookup_comparison_operator(expression.operator)
            expression_01 = self._parse_expression(expression.expr1)
            expression_02 = self._parse_expression(expression.expr2)
            if not expression_01:
                relevance_qry = "{}".format(expression_02)

            elif not expression_02:
                relevance_qry = "{}".format(expression_01)
            else:
                relevance_qry = "{} {} {}".format(expression_01, operator, expression_02)
            return relevance_qry
        elif isinstance(expression, ObservationExpression):
            self.__eval_observation_exp(expression, qualifier)
            return None
        elif isinstance(expression, CombinedObservationExpression):
            self._parse_expression(expression.expr1, qualifier)
            self._parse_expression(expression.expr2, qualifier)
            return None
        elif isinstance(expression, StartStopQualifier):
            if hasattr(expression, 'observation_expression'):
                return self._parse_expression(getattr(expression, 'observation_expression'), expression.qualifier)
        elif isinstance(expression, Pattern):
            return self._parse_expression(expression.expression)
        else:
            raise RuntimeError("Unknown Recursion Case for expression={}, type(expression)={}".format(
                expression, type(expression)))

    def __eval_comparison_exp(self, expression):
        """
        Function for parsing comparsion expression and returning the relevance query
        :param expression: expression object, ANTLR parsed expression object
        :return: str, relevance query string for the comparison expression
        """
        self._relevance_string_list = []
        conditional_attr_dict = {'creator_user_ref': 'user'}
        stix_object, stix_field = expression.object_path.split(':')
        conditional_attr = conditional_attr_dict.get(stix_field.split('.')[0], None)
        mapped_fields_array = self.dmm.map_field(stix_object, stix_field)
        comparator = self._lookup_comparison_operator(expression.comparator)
        value = self._html_encoding_escape_character(expression.value)
        if expression.comparator == ComparisonComparators.In:
            value = self._format_set(value)
        elif expression.comparator in [ComparisonComparators.Equal, ComparisonComparators.NotEqual,
                                       ComparisonComparators.GreaterThan,
                                       ComparisonComparators.GreaterThanOrEqual, ComparisonComparators.LessThan,
                                       ComparisonComparators.LessThanOrEqual]:
            value = self._format_equality(value)
        # '%' -> '*' wildcard, '_' -> '?' single wildcard
        elif expression.comparator == ComparisonComparators.Like:
            value = self._format_like(value)
        elif expression.comparator == ComparisonComparators.Matches:
            value = self._format_matches(value)
        else:
            raise NotImplementedError("Unknown comparison operator {}.".format(expression.comparator))
        self.get_field_relevance_qry(mapped_fields_array[0].split('.')[0], self._master_obj)
        comparison_string = self._parse_mapped_fields(value, comparator,
                                                      mapped_fields_array, conditional_attr, bool(expression.negated))
        if '{}.{}'.format(FILE, SEARCH_FOLDER) in mapped_fields_array:
            self.search_folder = value
        else:
            comparison_string = self.clean_format_string(comparison_string)
        if expression.negated:
            comparison_string = self._negate_comparison(comparison_string, comparator)
        # Assigning the relevance condition of mac address to an instance variable and returning ''
        # so as to convert into individual API relevance query
        _is_expr_split_needed, is_expr_modified = self._is_exp_split_needed(expression)
        if _is_expr_split_needed:
            if is_expr_modified:
                comparison_string = self.__eval_comparison_exp(expression)
            self._relevance_query_for_split_attr.append(comparison_string)
            comparison_string = ''
        return "{}".format(comparison_string)

    def __eval_obs_exp_subroutine(self, relevance_query, qualifier):
        """
        A sub method call for __eval_obs_exp to aid in final relevance query formation
        :param relevance_query: str
        :param qualifier: str | None
        :return: str
        """
        relevance_qry_termination_string = {
            FILE:
                {
                    "add_qry_closing_string": 1,
                    "format_string": " of {} {}"
                },
            PROCESS:
                {
                    "add_qry_closing_string": 1,
                    "format_string": ""
                },
            SOCKET:
                {
                    "add_qry_closing_string": 1,
                    "format_string": " of {}"
                },

            ADAPTER:
                {
                    "add_qry_closing_string": 1,
                    "format_string": " of {}"
                },
        }
        condition_addition_for_split_attr = {ADAPTER: ['loopback of it = false', 'address of it != "0.0.0.0"']}
        self.qualifier_string = self._parse_time_range(qualifier, self._master_obj,
                                                       self._relevance_property_format_string_dict,
                                                       self._time_range, self._time_range_comparator_list)
        self.qualifier_string = self.clean_format_string(self.qualifier_string)
        if self.qualifier_string:
            # Apply the time range to entire observation expression
            if relevance_query:
                relevance_query = '({})'.format(relevance_query)
                relevance_query += ' AND ' + self.qualifier_string
            else:
                relevance_query += self.qualifier_string
        if self._master_obj in condition_addition_for_split_attr:
            relevance_query += ' AND '+'({})'.format(' AND '.join(
                condition_addition_for_split_attr.get(self._master_obj)))
        relevance_query = WHOSE_STRING.format(relevance_query) if relevance_query else ''
        closing_relevance_string = relevance_qry_termination_string.get(self._master_obj).get('format_string') if \
            relevance_qry_termination_string.get(self._master_obj).get('add_qry_closing_string') and \
            relevance_qry_termination_string.get(self._master_obj).get('format_string') else ""
        if self._master_obj == FILE:
            closing_relevance_string = closing_relevance_string.format(
                *('', self.search_folder) if (self.search_folder == DEFAULT_SEARCH_FOLDER)
                else (SEARCH_FOLDER, self.search_folder))
        elif self._master_obj in [SOCKET, ADAPTER]:
            closing_relevance_string = closing_relevance_string.format(NETWORK)
        final_comparison_exp = self.clean_format_string(self._stix_object_format_string_lookup_dict.
                                                        get(self._master_obj)).format(relevance_query)
        final_comparison_exp += closing_relevance_string
        return final_comparison_exp

    def __eval_observation_exp(self, expression, qualifier):
        """
        Function for parsing observation expression and form the complete relevance query
        :param expression: expression object, ANTLR parsed expression object
        :param qualifier: str | None
        :return: None
        """
        # Initializing all instance variable at observation expression level
        self._master_obj = None
        self._split_master_obj_list = []
        self._relevance_query_for_split_attr = []
        self.search_folder = DEFAULT_SEARCH_FOLDER
        objects_hierarchy_dict = self._relevance_property_format_string_dict.get('object_hierarchy')
        objects_list = list(objects_hierarchy_dict.keys())
        self.get_master_obj_of_obs_exp(expression.comparison_expression, objects_list)
        relevance_query = self._parse_expression(expression.comparison_expression)
        if self._master_obj:
            final_comparison_exp = self.__eval_obs_exp_subroutine(relevance_query, qualifier)
            self.qualified_queries.append(final_comparison_exp)
        # Below code is for splitting the observation expression into multiple observation expression
        # in the event of mac address attribute provided as input along with other attributes
        if self._relevance_query_for_split_attr:
            for index, each_obj in enumerate(self._split_master_obj_list):
                self._master_obj = each_obj
                final_comparison_exp = self.__eval_obs_exp_subroutine(self._relevance_query_for_split_attr[index],
                                                                      qualifier)
                self.qualified_queries.append(final_comparison_exp)

    def parse_expression(self, pattern: Pattern):
        """
        parse_expression --> Native query
        :param pattern: expression object, ANTLR parsed expression object
        :return:str, relevance query(native query)
        """
        return self._parse_expression(pattern)


def translate_pattern(pattern: Pattern, data_model_mapper, options):
    """
    Conversion of expression object to XML query
    :param pattern: expression object, ANTLR parsed expression object
    :param data_model_mapper: DataMapper object, mapping object obtained by parsing from_stix_map.json
    :param options: dict, contains 2 keys result_limit defaults to 10000, time_range defaults to 5
    :return: str, XML query with relevance query embedded inside <QueryText> tag
    """
    time_range = options['time_range']
    list_final_query = []
    translated_dictionary = RelevanceQueryStringPatternTranslator(pattern, data_model_mapper, time_range)
    final_query = translated_dictionary.qualified_queries
    for each_query in final_query:
        besapi_query = '<BESAPI xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xsi:' \
                       'noNamespaceSchemaLocation=\"BESAPI.xsd\"><ClientQuery>' \
                       '<ApplicabilityRelevance>true</ApplicabilityRelevance><QueryText>' + each_query + \
                       '</QueryText><Target><CustomRelevance>true</CustomRelevance></Target></ClientQuery></BESAPI>'
        list_final_query.append(besapi_query)
    return list_final_query
