import re
import json
import datetime
import copy
from stix_shifter_utils.stix_translation.src.patterns.pattern_objects import ObservationExpression, ComparisonExpression, \
    ComparisonExpressionOperators, ComparisonComparators, Pattern, \
    CombinedComparisonExpression, CombinedObservationExpression, ObservationOperators
from stix_shifter_modules.guardium.stix_translation.transformers import TimestampToGuardium
from stix_shifter_utils.stix_translation.src.json_to_stix import observable
from stix_shifter_utils.utils.file_helper import read_json

# Source and destination reference mapping for ip and mac addresses.
# Change the keys to match the data source fields. The value array indicates the possible data type that can come into from field.
# REFERENCE_DATA_TYPES = {"QUERY_FROM_DATE": ["start"],
#                        "QUERY_TO_DATE": ["end"],"OSUser":["%"],"DBUser":"newuser",
#                        "SHOW_ALIASES":["TRUE","FALSE"],"REMOTE_SOURCE":["%"]}
DEFAULT_DAYS_BACK = 2


class QueryStringPatternTranslator:
    # Change comparator values to match with supported data source operators
    comparator_lookup = {
        ComparisonExpressionOperators.And: "AND",
        ComparisonExpressionOperators.Or: "OR",
        #        ComparisonComparators.GreaterThan: ">",
        #        ComparisonComparators.GreaterThanOrEqual: ">=",
        #        ComparisonComparators.LessThan: "<",
        #        ComparisonComparators.LessThanOrEqual: "<=",
        ComparisonComparators.Equal: "=",
        #        ComparisonComparators.NotEqual: "!=",
        #        ComparisonComparators.Like: "LIKE",
        #        ComparisonComparators.In: "IN",
        #        ComparisonComparators.Matches: 'LIKE',
        # ComparisonComparators.IsSubSet: '',
        # ComparisonComparators.IsSuperSet: '',
        ObservationOperators.Or: 'OR',
        # Treat AND's as OR's -- Unsure how two ObsExps wouldn't cancel each other out.
        ObservationOperators.And: 'OR'
    }

    def __init__(self, pattern: Pattern, data_model_mapper, options, transformers):
        self.dmm = data_model_mapper
        self.pattern = pattern
        # Now report_params_passed is a JSON object which is pointing to an array of JSON Objects (report_params_array)
        self.report_params_passed = {}
        self.report_params_array = []
        self.report_params_array_size = 0

        # Now qsearch_params_passed is a JSON object which is pointing to an array of JSON Objects (qsearch_params_array)
        self.qsearch_params_passed = {}
        self.qsearch_params_array = []
        self.qsearch_params_array_size = 0

        self.translated = self.parse_expression(pattern)
        self.transformers = transformers

        # Read reference data
        self.REFERENCE_DATA_TYPES = read_json('reference_data_types4Query', options)

        # Read report definition data
        self.REPORT_DEF = read_json('guardium_reports_def', options)

        # Read report definition data
        self.REPORT_PARAMS_MAP = read_json('guardium_report_params_map', options)

        # Read qsearch definition data
        self.QSEARCH_DEF = read_json('guardium_qsearch_def', options)

        # Read qsearch definition data
        self.QSEARCH_PARAMS_MAP = read_json('guardium_qsearch_params_map', options)

    def set_report_params_passed(self, params_array):
        self.report_params_array = params_array
        self.report_params_array_size = len(params_array)
        return

    def set_qsearch_params_passed(self, params_array):
        self.qsearch_params_array = params_array
        self.qsearch_params_array_size = len(params_array)
        return

    def transform_report_call_to_json(self, report_call):
        # Convert the report call (string) into an array of JSON.  Note, inside each json obj multiple key/value parmeter are "OR"
        # Where as each key/value parameter from two json objects are "AND"
        # Put quote around key
        # print(report_call)
        regex = r"([a-zA-Z_]+)(\s=)"
        out_str = re.sub(regex, r"'\1' :", report_call, 0)

        # Create the Json structure
        regex1 = r"\(|\)"
        out_str = re.sub(regex1, "", out_str, 0)
        regex2 = r"\sAND\s"
        out_str = "{" + re.sub(regex2, "} AND {", out_str, 0) + "}"
        regex3 = r"START"
        out_str = re.sub(regex3, "} AND {START ", out_str, 0)
        # treat START and STOP parameters too
        regex4 = r"(START|STOP)"
        out_str = re.sub(regex4, r"'\1' : ", out_str, 0)
        regex5 = r"([Z\'\s]+STOP)"
        out_str = re.sub(regex5, r"'} AND {'STOP", out_str, 0)
        regex6 = r"(START|STOP)\'[\s\:t\']+"
        out_str = re.sub(regex6, r"\1' : '", out_str, 0)

        # Finalize the structure -- replace by comma and then it becomes string containing
        # an array of Json objects
        regex7 = r"\sOR|\sAND"
        out_str = re.sub(regex7, r",", out_str, 0)

        # Single quotes have to be replaced by double quotes in order to make it as an Json obj
        regex8 = r"'"
        out_str = "[" + re.sub(regex8, '"', out_str, 0) + "]"

        return json.loads(out_str)

    def transform_qsearch_call_to_json(self, qsearch_call):
        # Convert the report call (string) into an array of JSON.  Note, inside each json obj multiple key/value parmeter are "OR"
        # Where as each key/value parameter from two json objects are "AND"
        # Put quote around key
        # print(report_call)
        regex = r"(^|\(|OR |AND )([a-zA-Z_ ]+)(\s=)"
        out_str = re.sub(regex, r"\1'\2' :", qsearch_call, 0)

        # Create the Json structure
        regex1 = r"\(|\)"
        out_str = re.sub(regex1, "", out_str, 0)
        regex2 = r"\sAND\s"
        out_str = "{" + re.sub(regex2, "} AND {", out_str, 0) + "}"
        regex3 = r"START"
        out_str = re.sub(regex3, "} AND {START ", out_str, 0)
        # treat START and STOP parameters too
        regex4 = r"(START|STOP)"
        out_str = re.sub(regex4, r"'\1' : ", out_str, 0)
        regex5 = r"([Z\'\s]+STOP)"
        out_str = re.sub(regex5, r"'} AND {'STOP", out_str, 0)
        regex6 = r"(START|STOP)\'[\s\:t\']+"
        out_str = re.sub(regex6, r"\1' : '", out_str, 0)

        # Finalize the structure -- replace by comma and then it becomes string containing
        # an array of Json objects
        regex7 = r"\sOR|\sAND"
        out_str = re.sub(regex7, r",", out_str, 0)

        # Single quotes have to be replaced by double quotes in order to make it as an Json obj
        regex8 = r"'"
        out_str = "[" + re.sub(regex8, '"', out_str, 0) + "]"

        return json.loads(out_str)

    # Guardium report parameters are "AND"ed in a Gaurdium query.
    # Our Json object array contains multiple json objects.  Each object may have one or many key/value pairs -- these are report params
    # Problem statement: get an array of json objects containing parameters which support a guardium report call
    def build_array_of_guardium_report_params(self, result_array, result_position, current_result_object, params_array, current_position):
        param_list_size = len(params_array)
        if current_result_object is None:
            current_result_object = {}
        if current_position is None:
            current_position = 0
        else:
            current_position = current_position + 1

        if current_position < param_list_size:
            param_json_object = params_array[current_position]
            for param in param_json_object:
                # Keep a copy of current_result_object before any modification from this invocation
                cp_current_result_object = copy.deepcopy(current_result_object)
                # Insert the param in the current_result_object
                if param not in cp_current_result_object:
                    cp_current_result_object[param] = param_json_object[param]
                    if (current_position + 1) < param_list_size:
                        result_array = self.build_array_of_guardium_report_params(result_array, result_position, cp_current_result_object, params_array, current_position)
                    else:
                        result_array.append(cp_current_result_object)
                        result_position = result_position + 1
        return result_array

    def build_array_of_guardium_qsearch_params(self, result_array, result_position, current_result_object, params_array, current_position):
        param_list_size = len(params_array)
        if current_result_object is None:
            current_result_object = {}
        if current_position is None:
            current_position = 0
        else:
            current_position = current_position + 1

        if current_position < param_list_size:
            param_json_object = params_array[current_position]
            for param in param_json_object:
                # Keep a copy of current_result_object before any modification from this invocation
                cp_current_result_object = copy.deepcopy(current_result_object)
                # Insert the param in the current_result_object
                if param not in cp_current_result_object:
                    cp_current_result_object[param] = param_json_object[param]
                    if (current_position + 1) < param_list_size:
                        result_array = self.build_array_of_guardium_qsearch_params(result_array, result_position, cp_current_result_object, params_array, current_position)
                    else:
                        result_array.append(cp_current_result_object)
                        result_position = result_position + 1
        return result_array

    def substitute_params_passed(self, report_definitions, reports_in_query):
        #   for Each report in report_definitions substitute params for report Params Passed
        #   generate all reports for the query
        #   In the event START and STOP is missing, Generate the default From and To Dates
        #   TO_DATE IS SET TO NOW
        #   FROM_DATE IS SET TO DAYS FROM NOW
        current_date = datetime.datetime.now()
        default_to_date = current_date.strftime(('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z')
        default_from_date = (current_date - datetime.timedelta(days=DEFAULT_DAYS_BACK)).strftime(('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z')
        for report_name in report_definitions:
            report = report_definitions[report_name]
            for param in report["reportParameter"]:
                # either the value will be default or passed in (report parameter passed)
                if param not in self.report_params_passed:
                    value = report["reportParameter"][param]["default"]
                else:
                    value = self.report_params_passed[param]
                # Use START and STOP  instead of default to time parameter
                if report["reportParameter"][param]["info"] == "START":
                    value = self.report_params_passed.get("START", default_from_date)
                if report["reportParameter"][param]["info"] == "STOP":
                    value = self.report_params_passed.get("STOP", default_to_date)
                # Transform the value or use it as-is
                if "transformer" in report["reportParameter"][param]:
                    transformer = self.transformers[report["reportParameter"][param]["transformer"]]
                    report["reportParameter"][param] = transformer.transform(value)
                else:
                    report["reportParameter"][param] = value

            reports_in_query.append(json.dumps(report))
        return reports_in_query

    def substitute_qsearch_params_passed(self, qsearch_definitions, qsearch_in_query):
        #   for Each report in report_definitions substitute params for report Params Passed
        #   generate all reports for the query
        #   In the event START and STOP is missing, Generate the default From and To Dates
        #   TO_DATE IS SET TO NOW
        #   FROM_DATE IS SET TO DAYS FROM NOW
        current_date = datetime.datetime.now()
        default_to_date = current_date.strftime(('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z')
        default_from_date = (current_date - datetime.timedelta(days=DEFAULT_DAYS_BACK)).strftime(('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z')
        for qsearch_name in qsearch_definitions:
            qsearch = qsearch_definitions[qsearch_name]

            sta = self.qsearch_params_passed.get("START", default_from_date)
            sto = self.qsearch_params_passed.get("STOP", default_to_date)
            qsearch["startTime"] = self.transformers[qsearch["startTime"]["transformer"]].transform(sta)
            qsearch["endTime"] = self.transformers[qsearch["endTime"]["transformer"]].transform(sto)

            for param in qsearch["filters"]:
                # either the value will be default or passed in (report parameter passed)
                if param not in self.qsearch_params_passed:
                    value = qsearch["filters"][param]["default"]
                else:
                    value = self.qsearch_params_passed[param]
                # Transform the value or use it as-is
                if "transformer" in qsearch["filters"][param]:
                    transformer = self.transformers[qsearch["filters"][param]["transformer"]]
                    qsearch["filters"][param] = transformer.transform(value)
                else:
                    qsearch["filters"][param] = value
            for param in qsearch["query"]:
                if param in self.qsearch_params_passed:
                    value = self.qsearch_params_passed[param]
                    if "transformer" in qsearch["query"][param]:
                        transformer = self.transformers[qsearch["query"][param]["transformer"]]
                        qsearch["query"][param]["value"] = transformer.transform(value)
                        qsearch["query"][param]["operation"] = qsearch["query"][param]["default_operator"]
            qsearch_in_query.append(json.dumps(qsearch))
        return qsearch_in_query

    def get_report_params(self):
        reports_in_query = []
        for report_param_index in range(self.report_params_array_size):
            self.report_params_passed = self.report_params_array[report_param_index]
            data_category = (self.report_params_passed).get("datacategory", None)
            if(data_category is not None):
                if data_category not in self.REPORT_DEF:
                    report_definitions = None
                else:
                    report_definitions = copy.deepcopy(self.REPORT_DEF[data_category])
            else:
                report_definitions = self.generate_report_definitions()
            # substitute Params
            if report_definitions:
                reports_in_query = self.substitute_params_passed(report_definitions, reports_in_query)
        return reports_in_query

    def get_qsearch_params(self):
        qsearch_in_query = []
        for qsearch_param_index in range(self.qsearch_params_array_size):
            self.qsearch_params_passed = self.qsearch_params_array[qsearch_param_index]
            #clientip = self.qsearch_params_passed.get("Client", None)
            #if clientip is not None:
            #    continue
            data_category = self.qsearch_params_passed.get("datacategory", None)
            if data_category is not None:
                if data_category not in self.QSEARCH_DEF:
                    qsearch_definitions = None
                else:
                    qsearch_definitions = copy.deepcopy(self.QSEARCH_DEF[data_category])
            else:
                qsearch_definitions = self.generate_qsearch_definitions()
            # substitute Params
            if qsearch_definitions:
               qsearch_in_query = self.substitute_qsearch_params_passed(qsearch_definitions, qsearch_in_query)

        self.set_filters_format(qsearch_in_query)
        self.set_query_format(qsearch_in_query)
        return qsearch_in_query

    def set_filters_format(self, qse):
        for i in range(len(qse)):
            filters = json.loads(qse[i])["filters"]
            qse_prefix = qse[i][0:str.find(qse[i], "filters") - 1:1]
            qse_suffix = qse[i][str.find(qse[i], ", \"query")::1]
            str_filters = ''
            first = True
            for key in filters:
                if filters[key] == '*':
                    continue
                if first:
                    first = False
                else:
                    str_filters = str_filters + "&"
                str_filters = str_filters + "name=" + key + "&" + "value=" + filters[key] + "&isGroup=false"
            if str_filters.__len__() > 0:
                str_filters = "\"filters\":\"" + str_filters + "\""
                qse[i] = qse_prefix + str_filters + qse_suffix
            else:
                qse[i] = qse_prefix + qse_suffix[2::1]

    def set_query_format(self, qse):
        for i in range(len(qse)):
            query = json.loads(qse[i])["query"]
            qse_prefix = qse[i][0:str.find(qse[i], "query") - 1:1]
            qse_suffix = qse[i][str.find(qse[i], ", \"fetchSize")::1]
            str_query = ''
            first = True
            for key in query:
                if "value" not in query[key]:
                    continue
                if first:
                    first = False
                else:
                    str_query = str_query + " AND "
                str_query = str_query +  key + query[key]["operation"] +query[key]["value"] 
            if str_query.__len__() > 0:
                str_query = "\"query\":\"" + str_query + "\""
                qse[i] = qse_prefix + str_query + qse_suffix
            else:
                qse[i] = qse_prefix + qse_suffix[2::1]

    def generate_report_definitions(self):
        # for Each param passed get all reports pertaining to that params  -- this is a set of param reports
        # then take intersection of each set
        # if the intersection is null use the default Category
        report_set = None
        param_map = self.REPORT_PARAMS_MAP["maps"]
        param_cmn = self.REPORT_PARAMS_MAP["common"]

        for param in self.report_params_passed:
            if param in param_map:
                param_set = set(param_map[param])
            elif param in param_cmn:
                param_set = set(self.REPORT_PARAMS_MAP["defaultReports"])
            else:
                param_set = None

# find interaction
# param_set
            if param_set is not None:
                if report_set is None:
                    report_set = set(param_set)
                else:
                    report_set = report_set.intersection(param_set)

        # Check if report_set is null
        if (not bool(report_set)):
            report_set = self.REPORT_PARAMS_MAP["defaultReports"]

        # Now we have to create report_definitions from this report_set
        # Report set --> data_category:report_name
        # Iterate through report_definitions and pick the reports and place them in the report Defs
        #
        report_definitions = {}

        for key in report_set:
            data_category, report = key.split(":")

            '''if data_category not in self.REPORT_DEF:
                raise RuntimeError(
                    "Error in parameter mapping file (data category): " + str(data_category) + " not there. Ingored.")
            else:'''
            data_category_reports = copy.deepcopy(self.REPORT_DEF[data_category])

            '''if report not in data_category_reports:
                    raise RuntimeError(
                        "Error in parameter mapping file (report name): " + str(report) + " not there. Ingored.")
                else:'''
            report_definitions[report] = data_category_reports[report]

        return report_definitions

    def generate_qsearch_definitions(self):
        # for Each param passed get all qsearchs pertaining to that params  -- this is a set of param qsearchs
        # then take intersection of each set
        # if the intersection is null use the default Category
        qsearch_set = None
        param_map = self.QSEARCH_PARAMS_MAP["maps"]
        param_cmn = self.QSEARCH_PARAMS_MAP["common"]

        for param in self.qsearch_params_passed:
            if param in param_map:
                param_set = set(param_map[param])
            elif param in param_cmn:
                param_set = set(self.QSEARCH_PARAMS_MAP["defaultQsearch"])
            else:
                param_set = None

            # find interaction
            # param_set
            if param_set is not None:
                if qsearch_set is None:
                    qsearch_set = set(param_set)
                else:
                    qsearch_set = qsearch_set.intersection(param_set)

        # Check if qsearch_set is null
        if (not bool(qsearch_set)):
            qsearch_set = self.QSEARCH_PARAMS_MAP["defaultQsearch"]

        # Now we have to create qsearch_definitions from this qsearch_set
        # Qsearch set --> data_category:qsearch_name
        # Iterate through qsearch_definitions and pick the qsearchs and place them in the qsearch Defs
        #
        qsearch_definitions = {}

        for key in qsearch_set:
            data_category, qsearch = key.split(":")

            ''' if data_category not in self.QSEARCH_DEF:
                raise RuntimeError(
                    "Error in parameter mapping file (data category): " + str(
                        data_category) + " not there. Ingored.")
            else:'''
            data_category_qsearch = copy.deepcopy(self.QSEARCH_DEF[data_category])

            '''if qsearch not in data_category_qsearch:
                    raise RuntimeError(
                        "Error in parameter mapping file (qsearch name): " + str(qsearch) + " not there. Ingored.")
                else: '''
            qsearch_definitions[qsearch] = data_category_qsearch[qsearch]

        return qsearch_definitions

    @staticmethod
    def _format_set(values) -> str:
        gen = values.element_iterator()
        return "({})".format(' OR '.join([QueryStringPatternTranslator._escape_value(value) for value in gen]))

    @staticmethod
    def _format_match(value) -> str:
        raw = QueryStringPatternTranslator._escape_value(value)
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
        value = "'%{value}%'".format(value=value)
        return QueryStringPatternTranslator._escape_value(value)

    @staticmethod
    def _escape_value(value, comparator=None) -> str:
        if isinstance(value, str):
            return '{}'.format(value.replace('\\', '\\\\').replace('\"', '\\"').replace('(', '\\(').replace(')', '\\)'))
        else:
            return value

    @staticmethod
    def _negate_comparison(comparison_string):
        return "NOT({})".format(comparison_string)

    @staticmethod
    def _check_value_type(value):
        value = str(value)
        for key, pattern in observable.REGEX.items():
            if key != 'date' and bool(re.search(pattern, value)):
                return key
        return None

    @staticmethod
    def _parse_reference(self, stix_field, value_type, mapped_field, value, comparator):
        if value_type not in self.REFERENCE_DATA_TYPES["{}".format(mapped_field)]:
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
                comparison_string += "{mapped_field} {comparator} {value}".format(mapped_field=mapped_field, comparator=comparator, value=value)
                #self.report_params_passed[mapped_field] = str(value).replace("'","",10)

            if (mapped_fields_count > 1):
                comparison_string += " OR "
                mapped_fields_count -= 1

        return comparison_string

    @staticmethod
    def _is_reference_value(stix_field):
        return stix_field == 'src_ref.value' or stix_field == 'dst_ref.value'

    def _parse_expression(self, expression, qualifier=None) -> str:
        if isinstance(expression, ComparisonExpression):  # Base Case
            # Resolve STIX Object Path to a field in the target Data Model
            stix_object, stix_field = expression.object_path.split(':')
            # Multiple data source fields may map to the same STIX Object
            mapped_fields_array = self.dmm.map_field(stix_object, stix_field)
            # Resolve the comparison symbol to use in the query string (usually just ':')
            comparator = self.comparator_lookup[expression.comparator]

            if stix_field == 'start' or stix_field == 'end':
                transformer = TimestampToGuardium()
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

            comparison_string = self._parse_mapped_fields(self, expression, value, comparator, stix_field, mapped_fields_array)
            if(len(mapped_fields_array) > 1 and not self._is_reference_value(stix_field)):
                # More than one data source field maps to the STIX attribute, so group comparisons together.
                grouped_comparison_string = "(" + comparison_string + ")"
                comparison_string = grouped_comparison_string

            if expression.comparator == ComparisonComparators.NotEqual:
                comparison_string = self._negate_comparison(comparison_string)

            if expression.negated:
                comparison_string = self._negate_comparison(comparison_string)
            if qualifier is not None:
                return "{} {}".format(comparison_string, qualifier)
            else:
                return "{}".format(comparison_string)

        elif isinstance(expression, CombinedComparisonExpression):
            operator = self.comparator_lookup[expression.operator]
            expression_01 = self._parse_expression(expression.expr1)
            expression_02 = self._parse_expression(expression.expr2)
            if not expression_01 or not expression_02:
                return ''
            if isinstance(expression.expr1, CombinedComparisonExpression):
                expression_01 = "({})".format(expression_01)
            if isinstance(expression.expr2, CombinedComparisonExpression):
                expression_02 = "({})".format(expression_02)
            query_string = "{} {} {}".format(expression_01, operator, expression_02)
            if qualifier is not None:
                return "{} {}".format(query_string, qualifier)
            else:
                return "{}".format(query_string)
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
            expression_01 = self._parse_expression(expression.expr1)
            expression_02 = self._parse_expression(expression.expr2)
            if expression_01 and expression_02:
                return "({}) {} ({})".format(expression_01, operator, expression_02)
            elif expression_01:
                return "{}".format(expression_01)
            elif expression_02:
                return "{}".format(expression_02)
            else:
                return ''
        elif isinstance(expression, Pattern):
            return "{expr}".format(expr=self._parse_expression(expression.expression))
        else:
            raise RuntimeError("Unknown Recursion Case for expression={}, type(expression)={}".format(
                expression, type(expression)))

    def parse_expression(self, pattern: Pattern):
        return self._parse_expression(pattern)


def translate_pattern(pattern: Pattern, data_model_mapping, options, transformers):

    # Converting query object to datasource query
    # timerange set to 24 hours for Guardium; timerange is provided in minutes (as delta)

    guardium_query_translator = QueryStringPatternTranslator(pattern, data_model_mapping, options, transformers)
    report_call = guardium_query_translator.translated

    # Add space around START STOP qualifiers
    report_call = re.sub("START", "START ", report_call)
    report_call = re.sub("STOP", " STOP ", report_call)

# Subroto: I did not change the code much just adapted to get the report parameters
# Subroto: added code to support report search parameters are "and" when sent to Guardium
    # translate the structure of report_call
    if data_model_mapping.dialect == 'report':
        json_report_call = guardium_query_translator.transform_report_call_to_json(report_call)
    else:
        json_qsearch_call = guardium_query_translator.transform_qsearch_call_to_json(report_call)

    result_array = []
    result_position = 0

    if data_model_mapping.dialect == 'report':
        output_array = guardium_query_translator.build_array_of_guardium_report_params(result_array, result_position, None, json_report_call, None)
        guardium_query_translator.set_report_params_passed(output_array)
        report_header = guardium_query_translator.get_report_params()
    else:
        output_array = guardium_query_translator.build_array_of_guardium_qsearch_params(result_array, result_position, None, json_qsearch_call, None)
        guardium_query_translator.set_qsearch_params_passed(output_array)
        report_header = guardium_query_translator.get_qsearch_params()

    if report_header:
        # Change return statement as required to fit with data source query language.
        # If supported by the language, a limit on the number of results may be desired.
        # A single query string, or an array of query strings may be returned
        return report_header
    else:
        # report_header = {"ID": 2000, "message": "Could not generate query -- issue with data_category."}
        return report_header
