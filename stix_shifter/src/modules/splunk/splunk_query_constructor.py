import logging
import re
from datetime import datetime

logger = logging.getLogger(__name__)

from stix_shifter.src.patterns.pattern_objects import ObservationExpression, ComparisonExpression, \
    ComparisonExpressionOperators, ComparisonComparators, Pattern, \
    CombinedComparisonExpression, CombinedObservationExpression, ObservationOperators
from stix_shifter.src.modules.car.car_data_mapping import CarDataMapper

from . import encoders
from . import object_scopers

class SplunkSearchTranslator:
    """ The core translator class. Instances should not be re-used """

    implemented_operators = {
        ObservationOperators.And: '{expr1} OR {expr2}',
        ObservationOperators.Or: '{expr1} OR {expr2}',
        # FollowedBy could also be done with transactions, however the original event would not be returned, though a
        # all the fields in the original event would be present in the transaction result.
        # For [x FOLLOWEDBY y], first find the most recent y, get its timestamp, and look for x's that occur earlier.
        # Use makeresults to inject a dummy event since a subsearch that yields no result will cause eval to error.
        # Presumably, no one will be looking for results prior to epoch=0.
        ObservationOperators.FollowedBy: "latest=[search {expr2} | append [makeresults 1 | eval _time=0]"
                                         "| head 1 | return $_time] | where {expr1}"
    }


    def __init__(self, pattern:Pattern, data_model_mapper, result_limit, timerange, object_scoper = object_scopers.default_object_scoper):
        self.dmm = data_model_mapper
        self.pattern = pattern
        self.object_scoper = object_scoper
        self._pattern_prefix = ""  # How should the final SPL query string start.  By default, use ''
        self.result_limit = result_limit
        self.timerange = timerange

    def translate(self, expression, qualifier=None):
        """ This is the worker method for the translation. It can be passed any of the STIX2 AST classes and will turn
            them in to strings. It's called recursively and then the results are composed into the full query. """
        if isinstance(expression, Pattern):
            # Note: The following call to translate might alter the value of self._pattern_prefix.
            expr = self.translate(expression.expression, qualifier=qualifier)
            return "{prefix}{expr}".format(prefix=self._pattern_prefix, expr=expr)
        elif isinstance(expression, ObservationExpression):
            translator = _ObservationExpressionTranslator(expression, self.dmm, self.object_scoper)
            translated_query_str = translator.translate(expression.comparison_expression)
            if qualifier:
                # start time pattern
                st_pattern = r"(START'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z')"
                # stop time pattern
                et_pattern = r"(STOP'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z')"

                # find start and stop time from qualifier string
                st_arr = re.findall(st_pattern, qualifier)
                et_arr = re.findall(et_pattern, qualifier)
                
                stix_date_format = "%Y-%m-%dT%H:%M:%Sz"
                splunk_date_format = "%m/%d/%Y:%H:%M:%S" 
                earliest, latest = "", ""

                if st_arr:
                    # replace START and single quotes with empty char in date string
                    earliest     = re.sub(r"(START|')", '', st_arr[0] if st_arr else "")
                    earliest_obj = datetime.strptime(earliest, stix_date_format)
                    earliest_dt  = earliest_obj.strftime(splunk_date_format)
                
                if et_arr:
                    # replace STOP and single quotes with empty char in date string
                    latest     = re.sub(r"(STOP|')", '', et_arr[0] if et_arr else "")
                    latest_obj = datetime.strptime(latest, stix_date_format)
                    latest_dt  = latest_obj.strftime(splunk_date_format)

                # prepare splunk SPL query 
                if earliest and latest:
                    return '{query_string} earliest="{earliest}" latest="{latest}"'.format(query_string=translated_query_str, 
                                                                                     earliest=earliest_dt,
                                                                                     latest=latest_dt)
                elif earliest:
                    return '{query_string} earliest="{earliest}"'.format(query_string=translated_query_str, 
                                                                                     earliest=earliest_dt)
                elif latest:
                     return '{query_string} latest="{latest}"'.format(query_string=translated_query_str, 
                                                                                     latest=latest_dt)
                else:
                    raise NotImplementedError("Qualifier type not implemented")
            else:
                # Setting timerange value if START and STOP qualifiers are absent.
                return '{query_string} earliest="{earliest}" | head {result_limit}'.format(query_string=translated_query_str, 
                                                                                           earliest=self.timerange, 
                                                                                           result_limit=self.result_limit)


        elif isinstance(expression, CombinedObservationExpression):
            combined_expr_format_string = self.implemented_operators[expression.operator]
            if expression.operator == ObservationOperators.FollowedBy:
                self._pattern_prefix = "|eval "
            return combined_expr_format_string.format(expr1=self.translate(expression.expr1),
                                                      expr2=self.translate(expression.expr2))
        
        elif hasattr(expression, 'qualifier') and hasattr(expression, 'observation_expression'):
            if isinstance(expression.observation_expression, CombinedObservationExpression):
                expr_format_string = self.implemented_operators[expression.observation_expression.operator]
                # qualifier only needs to be passed into the parse expression once since it will be the same for both expressions
                return expr_format_string.format(expr1=self.translate(expression.observation_expression.expr1),
                                                 expr2=self.translate(expression.observation_expression.expr2, expression.qualifier))
            else:
               return self.translate(expression.observation_expression, expression.qualifier)
        else:
            raise NotImplementedError("Comparison type not implemented")


class _ObservationExpressionTranslator:

    _comparators = {
        ComparisonComparators.GreaterThan: ">",
        ComparisonComparators.GreaterThanOrEqual: ">=",
        ComparisonComparators.LessThan: "<",
        ComparisonComparators.LessThanOrEqual: "<=",
        ComparisonComparators.Equal: "=",
        ComparisonComparators.NotEqual: "!=",
        ComparisonComparators.Like: encoders.like,
        ComparisonComparators.In: encoders.set,
        ComparisonComparators.Matches: encoders.matches,
        ComparisonExpressionOperators.And: 'AND',
        ComparisonExpressionOperators.Or: 'OR',
        ComparisonComparators.IsSuperSet: "=", # Splunk cidrmatch('<ip in CIDR notation>', ip) and = operator give the same result
        ComparisonComparators.IsSubSet: "=" # cidrmatch function can be used for both issuperset and issubset operator
    }

    def __init__(self, expression:ObservationExpression, dmm, object_scoper):
        # Expression that we're converting
        self.expression = expression
        self.dmm = dmm
        self.object_scoper = object_scoper

    def translate(self, expression):
        if isinstance(expression, ComparisonExpression):
            stix_object, stix_path = expression.object_path.split(':')

            # These are the native objects and fields
            object_mapping = self.dmm.map_object(stix_object)
            field_mapping = self.dmm.map_field(stix_object, stix_path)
            # This scopes the query to the object
            object_scoping = self.object_scoper(object_mapping)

            # Check if mapping has multiple fields
            if isinstance(field_mapping, list):
                comparison_string = ""
                mapped_fields_count = len(field_mapping)
                for mapped_field in field_mapping:
                    # Returns the actual comparison (as a translated string)
                    comparison_string += self._build_comparison(expression, object_scoping, mapped_field)
                    if (mapped_fields_count > 1):
                        comparison_string += " OR "
                        mapped_fields_count -= 1

                if(len(field_mapping) > 1):
                    # More than one SPL field maps to the STIX attribute so group the ORs.
                    grouped_comparison_string = "(" + comparison_string + ")"
                    comparison_string = grouped_comparison_string
                    
                return comparison_string
            else:
                return self._build_comparison(expression, object_scoping, field_mapping)

        elif isinstance(expression, CombinedComparisonExpression):
            return "({} {} {})".format(
                self.translate(expression.expr1),
                self._comparators[expression.operator],
                self.translate(expression.expr2)
            )

    def _build_comparison(self, expression, object_scoping, field_mapping):
        if expression.comparator in self._comparators:
            comparator = self._comparators[expression.comparator]
            if isinstance(comparator, str):
                splunk_comparison = self._maybe_negate("{} {} {}".format(
                    field_mapping,
                    comparator,
                    encoders.simple(expression.value)
                ), expression.negated)

                return "({} AND {})".format(object_scoping, splunk_comparison)
            else:
                return "({} AND {})".format(
                    object_scoping,
                    self._maybe_negate(comparator(field_mapping, expression.value), expression.negated)
                )
        else:
            raise NotImplementedError("Haven't implemented comparator")

    def _maybe_negate(self, splunk_comparison, negated):
        if negated:
            return "NOT ({})".format(splunk_comparison)
        else:
            return splunk_comparison

def translate_pattern(pattern: Pattern, data_model_mapping, result_limit, timerange=None):
    # CAR + Splunk = we want to override the default object scoper, I guess?
    if isinstance(data_model_mapping, CarDataMapper):
        x = SplunkSearchTranslator(pattern, data_model_mapping, result_limit, timerange, object_scoper = object_scopers.car_object_scoper)
    else:
        x = SplunkSearchTranslator(pattern, data_model_mapping, result_limit, timerange)
    return x.translate(pattern)
