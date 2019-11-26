from stix_shifter.stix_translation.src.patterns.pattern_objects import ObservationExpression, ComparisonExpression, \
    ComparisonExpressionOperators, ComparisonComparators, Pattern, \
    CombinedComparisonExpression, CombinedObservationExpression, ObservationOperators
from stix_shifter.stix_translation.src.utils.transformers import TimestampToMilliseconds
from stix_shifter.stix_translation.src.utils.transformers import TimestampToGuardium
from stix_shifter.stix_translation.src.json_to_stix import observable
from stix_shifter.stix_translation.src.utils.stix_pattern_parser import parse_stix
from stix_shifter.stix_translation.src.utils import transformers
#
# Following added by Subroto
import re
import json
import array
import datetime
import re
import sys
import copy

# Source and destination reference mapping for ip and mac addresses.
# Change the keys to match the data source fields. The value array indicates the possible data type that can come into from field.
#REFERENCE_DATA_TYPES = {"QUERY_FROM_DATE": ["start"],
#                        "QUERY_TO_DATE": ["end"],"OSUser":["%"],"DBUser":"newuser",
#                        "SHOW_ALIASES":["TRUE","FALSE"],"REMOTE_SOURCE":["%"]}
REFERENCE_DATA_TYPES = {}


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
        ObservationOperators.Or: 'AND',
        # Treat AND's as OR's -- Unsure how two ObsExps wouldn't cancel each other out.
        ObservationOperators.And: 'AND'
    }

    def __init__(self, pattern: Pattern, data_model_mapper):
        self.dmm = data_model_mapper
        self.pattern = pattern
#
# Now reportParamsPassed is an json object which is pointing to an array of Json Objects (reportParamsArray)
        self.reportParamsPassed = {}
        self.reportParamsArray = []
        self.reportParamsArraySize = 0
        self.translated = self.parse_expression(pattern)
        self.transformers = transformers.get_all_transformers()
        #Read reference data
        with open("./stix_shifter/stix_translation/src/modules/guardium/json/reference_data_types4Query.json", 'r') as f_ref:
            self.REFERENCE_DATA_TYPES = json.loads(f_ref.read())
# Used in the future when custom STIX params could be used
        REFERENCE_DATA_TYPES = self.REFERENCE_DATA_TYPES

        #Read report definition data
        with open("./stix_shifter/stix_translation/src/modules/guardium/json/guardium_reports_def.json", 'r') as f_rep:
            self.REPORT_DEF = json.loads(f_rep.read())

        #Read report definition data
        with open("./stix_shifter/stix_translation/src/modules/guardium/json/guardium_report_params_map.json", 'r') as f_repm:
            self.REPORT_PARAMS_MAP = json.loads(f_repm.read())
#
    def set_ReportParamsPasseed(self, paramsArray):
        self.reportParamsArray = paramsArray
        self.reportParamsArraySize = len(paramsArray)
        return
#
    def trnsfReportCall2Json(self,repCall):
    # Convert repCall (string) into an array of JSON.  Note, inside each json obj multiple key/value parmeter are "OR"
    # Where as each key/value parameter from two json objects are "AND"
        #
        # Put quote around key
        print(repCall)
        regex = r"([a-zA-Z_]+)(\s=)"
        out_str = re.sub(regex, r"'\1' :", repCall,0)

        # Create the Json structure
        regex1 = r"\(|\)"
        out_str = re.sub(regex1, "", out_str,0)
#
        regex2 = r"\sAND\s"
        out_str = "{" + re.sub(regex2, "} AND {", out_str,0) + "}"
        #
        regex3 = r"START"
        out_str = re.sub(regex3, "} AND {START ", out_str,0)
        # treat START and STOP parameters too
        regex4 = r"(START|STOP)"
        out_str = re.sub(regex4, r"'\1' : ", out_str,0)
        #
        regex5 = r"([Z\'\s]+STOP)"
        out_str = re.sub(regex5, r"'} AND {'STOP", out_str,0)
        #
        regex6 = r"(T|P)\'[\s\:t]+"
        out_str = re.sub(regex6, r"\1' : ", out_str,0)

        #
        # Finalize the structure -- replace by comma and then it becomes string containing
        # an array of Json objects
        regex7 = r"\sOR|\sAND"
        out_str = re.sub(regex7, r",", out_str,0)

        # Single quotes have to be replaced by double quotes in order to make it as an Json obj
        regex8 = r"'"
        out_str = "[" + re.sub(regex8, '"', out_str,0) + "]"

        #
        jParams_def = json.loads(out_str)
        return jParams_def
    #
    # Guardium report parameters are "AND"ed in a Gaurdium query.
    # Our Json object array contains multiple json objects.  Each object may have one or many key/value paris -- these are report params
    # Problem statement: get an array of json objects containing parameters which support a guardium report call
    #
    def buildArrayOfGuardiumReportParams(self,resArray, resPos, curResObj, paramsArray, curPos):
        # initialize
        pArrSize = len(paramsArray)
        if curResObj is None:
            curResObj = {}
        if curPos is None:
            curPos = 0
        else:
            curPos = curPos + 1

        if curPos < pArrSize:
            thisJObj = paramsArray[curPos]
            #print(thisJObj)
        #
        # Iterate over this json Object
            for param in thisJObj:
                # Keep a copy of curResObj before any modification from this invocation
                cp_curResObj = copy.deepcopy(curResObj)
                # Insert the param in the curResObj
                print(param)
                if param not in cp_curResObj:
                    cp_curResObj[param] = thisJObj[param]
                    #print(cp_curResObj)
                    if (curPos + 1) < pArrSize:
                        resArray = self.buildArrayOfGuardiumReportParams(resArray, resPos, cp_curResObj, paramsArray, curPos)
                    else:
                        resArray.append(cp_curResObj)
                        resPos = resPos + 1
        #
        #print(resPos)
        #print(resArray)
        return resArray
    #
    def substitute_ParamsPassed(self, reportDefs, reports_in_query):
    # for Each report in reportDefs substitue params for report Params Passed
    #   generate all reports for the query
        for reportName in reportDefs:
            report = reportDefs[reportName]
            print(report)
            for param in report["reportParameter"]:
                print(param)
                # either the value will be default or passed by ISC (report parameter passed)
                if param not in self.reportParamsPassed:
                    value = report["reportParameter"][param]["default"]
                else:
                    value = self.reportParamsPassed[param]
                print(value)
                print(report["reportParameter"][param]["info"])
     #
     # Use START and STOP  instead of default to time parameter
                if report["reportParameter"][param]["info"] == "START":
                    value = self.reportParamsPassed["START"]
                    print("START")
                    print(value)
                if report["reportParameter"][param]["info"] == "STOP":
                    value = self.reportParamsPassed["STOP"]
                    print("STOP")
                    print(value)
      #
      #Transform the value or use it as-is
                if "transformer" in report["reportParameter"][param]:
                    transformer = self.transformers[report["reportParameter"][param]["transformer"]]
                    report["reportParameter"][param] = transformer.transform(value)
                else:
                    report["reportParameter"][param] = value

            reports_in_query.append(report)
#
        return reports_in_query
#
    def get_report_params(self):
        reports_in_query = []
        for repParamIndex in range(self.reportParamsArraySize):
            self.reportParamsPassed = self.reportParamsArray[repParamIndex]
            dataCategory = (self.reportParamsPassed).get("datacategory", None)
            if(dataCategory is not None):
                if dataCategory not in self.REPORT_DEF:
                    reportDefs = None
                else:
                    reportDefs = copy.deepcopy(self.REPORT_DEF[dataCategory])
    #
            else:
                reportDefs = self.generate_ReportDefs()
            # substitue Params
            reports_in_query = self.substitute_ParamsPassed(reportDefs,reports_in_query)

        return reports_in_query
# Report Defintions list
    def generate_ReportDefs(self):
    # for Each param passed get all reports pertaining to that params  -- this is a set of param reports
    # then take intersection of each set
    # if the intersection is null use the default Category
    #
        reportSet = None
        param_map = self.REPORT_PARAMS_MAP["maps"]
        param_cmn = self.REPORT_PARAMS_MAP["common"]

        for param in self.reportParamsPassed:
            if param in param_map:
                pSet = set(param_map[param])
            elif param in param_cmn:
                pSet = set(self.REPORT_PARAMS_MAP["defaultReports"])
            else:
                pSet = None

# find interaction
# pSet
            if pSet is not None:
                if reportSet is None:
                    reportSet = set(pSet)
                else:
                    reportSet = reportSet.intersection(pSet)
            #

        # Check if reportSet is null
        if (not bool(reportSet)):
            reportSet = self.REPORT_PARAMS_MAP["defaultReports"]
#

        # Now we have to create reportDefs from this reportSet
        # Report set --> dataCategory:reportName
        # Iterate through self.reportDefs and pick the reports and place them in the report Defs
        #
        reportDefs = {}

        for key in reportSet:
            dataCategory, report = key.split(":")

            if dataCategory not in self.REPORT_DEF:
                raise RuntimeError(
                        "Error in parameter mapping file (data category): " + str(dataCategory) + " not there. Ingored.")
            else:
                dcReports = copy.deepcopy(self.REPORT_DEF[dataCategory])

                if report not in dcReports:
                    raise RuntimeError(
                            "Error in parameter mapping file (report name): " + str(report) + " not there. Ingored.")
                else:
                    reportDefs[report] = dcReports[report]
            #

        return reportDefs

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
                comparison_string += "{mapped_field} {comparator} {value}".format(mapped_field=mapped_field, comparator=comparator, value=value)
                #self.reportParamsPassed[mapped_field] = str(value).replace("'","",10)

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
                #transformer = TimestampToMilliseconds()
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


def translate_pattern(pattern: Pattern, data_model_mapping, options):

    # Converting query object to datasource query
    # timerange set to 24 hours for Guardium; timerange is provided in minutes (as delta)
    timerange = 24 * 60 * 60
    parsed_stix = parse_stix(pattern,timerange)

#
    guardiumQueryTranslator = QueryStringPatternTranslator(pattern, data_model_mapping)
    reportCall = guardiumQueryTranslator.translated

    # Add space around START STOP qualifiers
    reportCall = re.sub("START", "START ", reportCall)
    reportCall = re.sub("STOP", " STOP ", reportCall)

#Subroto: I did not change the code much just adapted to get the report parameters
#Subroto: added code to support report search parameters are "and" when sent to Guardium
#
#   Limit recursive call to build an array of report parameters
#   Minimum is 500.
#   Increase the limit if required in the future; un-comment the line below and change the limit
#   sys.setrecursionlimit(500)
# translate the structure of reportCall that
    jRepCall = guardiumQueryTranslator.trnsfReportCall2Json(reportCall)

    resArray = []
    resPos = 0
    outArray = guardiumQueryTranslator.buildArrayOfGuardiumReportParams(resArray, resPos, None, jRepCall, None)
    guardiumQueryTranslator.set_ReportParamsPasseed(outArray)

    #
    # get report hearder -- multiple for
    reportHeader = guardiumQueryTranslator.get_report_params()
    if (reportHeader != None):
        # Change return statement as required to fit with data source query language.
        # If supported by the language, a limit on the number of results may be desired.
        # A single query string, or an array of query strings may be returned
        return "{}".format(reportHeader)
    else:
        reportHeader = {"ID":1001, "message": "Could not generate query -- issue with dataCategory."}
        return reportHeader
