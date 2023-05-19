import logging
import re
from datetime import datetime

logger = logging.getLogger(__name__)

from stix_shifter_utils.stix_translation.src.patterns.pattern_objects import ObservationExpression, ComparisonExpression, \
    ComparisonExpressionOperators, ComparisonComparators, Pattern, \
    CombinedComparisonExpression, CombinedObservationExpression, ObservationOperators
from stix_shifter_utils.modules.car.stix_translation.query_translator import CarBaseQueryTranslator

from . import encoders
from . import object_scopers


def stix_strptime(date_string):
    stix_date_format = "%Y-%m-%dT%H:%M:%S.%fz"
    stix_date_format_secs = "%Y-%m-%dT%H:%M:%Sz"
    try:
        return datetime.strptime(date_string, stix_date_format)
    except ValueError:
        return datetime.strptime(date_string, stix_date_format_secs)


def _needs_where_command(translated_query_str):
    return bool(re.search(r'(like|match)\(', translated_query_str))


class SplunkSearchTranslator:
    """ The core translator class. Instances should not be re-used """

    def __init__(self, pattern: Pattern, data_model_mapper, result_limit, time_range, object_scoper=object_scopers.default_object_scoper):
        self.dmm = data_model_mapper
        # FollowedBy could also be done with transactions, however the original event would not be returned, though a
        # all the fields in the original event would be present in the transaction result.
        # For [x FOLLOWEDBY y], first find the most recent y, get its timestamp, and look for x's that occur earlier.
        # Use makeresults to inject a placeholder event since a subsearch that yields no result will cause eval to error.
        # Presumably, no one will be looking for results prior to epoch=0.
        self.comparator_lookup = self.dmm.map_comparator()
        self.pattern = pattern
        self.object_scoper = object_scoper
        self._pattern_prefix = ""  # How should the final SPL query string start.  By default, use ''
        self.result_limit = result_limit
        self.time_range = time_range

    def translate(self, expression, qualifier=None):
        """ This is the worker method for the translation. It can be passed any of the STIX2 AST classes and will turn
            them in to strings. It's called recursively and then the results are composed into the full query. """
        if isinstance(expression, Pattern):
            # Note: The following call to translate might alter the value of self._pattern_prefix.
            expr = self.translate(expression.expression, qualifier=qualifier)
            return '{prefix}{expr}'.format(prefix=self._pattern_prefix, expr=expr)

        elif isinstance(expression, ObservationExpression):
            translator = _ObservationExpressionTranslator(expression, self.dmm, self.comparator_lookup, self.object_scoper)
            translated_query_str = translator.translate(expression.comparison_expression)

            if qualifier:
                # timestamp pattern according to STIX spec
                ts_pattern = r"t'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,6})?Z'"

                # start time pattern
                st_pattern = f"(START{ts_pattern})"
                # stop time pattern
                et_pattern = f"(STOP{ts_pattern})"

                # find start and stop time from qualifier string
                st_arr = re.findall(st_pattern, qualifier)
                et_arr = re.findall(et_pattern, qualifier)

                splunk_date_format = "%m/%d/%Y:%H:%M:%S"
                earliest, latest = "", ""

                if st_arr:
                    # replace START and single quotes with empty char in date string
                    earliest = re.sub(r"(STARTt|')", '', st_arr[0][0] if st_arr else "")
                    earliest_obj = stix_strptime(earliest)
                    earliest_dt = earliest_obj.strftime(splunk_date_format)

                if et_arr:
                    # replace STOP and single quotes with empty char in date string
                    latest = re.sub(r"(STOPt|')", '', et_arr[0][0] if et_arr else "")
                    latest_obj = stix_strptime(latest)
                    latest_dt = latest_obj.strftime(splunk_date_format)

                # prepare splunk SPL query
                if _needs_where_command(translated_query_str):
                    if earliest and latest:
                        return 'earliest="{earliest}" latest="{latest}" | where {query_string}'.format(query_string=translated_query_str,
                                                                                                       earliest=earliest_dt,
                                                                                                       latest=latest_dt)
                    elif earliest:
                        return 'earliest="{earliest}" | where {query_string}'.format(query_string=translated_query_str,
                                                                                     earliest=earliest_dt)
                    elif latest:
                        return 'latest="{latest}" | where {query_string}'.format(query_string=translated_query_str,
                                                                                 latest=latest_dt)
                    else:
                        raise NotImplementedError("Qualifier type not implemented")
                else:
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
                # Setting time_range value if START and STOP qualifiers are absent.
                return translated_query_str

        elif isinstance(expression, CombinedObservationExpression):
            combined_expr_format_string = self.comparator_lookup[str(expression.operator)]
            if expression.operator == ObservationOperators.FollowedBy:
                self._pattern_prefix = "|eval "
            return combined_expr_format_string.format(expr1=self.translate(expression.expr1),
                                                      expr2=self.translate(expression.expr2))

        elif hasattr(expression, 'qualifier') and hasattr(expression, 'observation_expression'):
            if isinstance(expression.observation_expression, CombinedObservationExpression):
                expr_format_string = self.comparator_lookup[str(expression.observation_expression.operator)]
                # qualifier only needs to be passed into the parse expression once since it will be the same for both expressions
                return expr_format_string.format(expr1=self.translate(expression.observation_expression.expr1),
                                                 expr2=self.translate(expression.observation_expression.expr2, expression.qualifier))
            else:
                return self.translate(expression.observation_expression, expression.qualifier)
        else:
            raise NotImplementedError("Comparison type not implemented")


class _ObservationExpressionTranslator:

    def __init__(self, expression: ObservationExpression, dmm, comparator_lookup, object_scoper):
        # Expression that we're converting
        self.expression = expression
        self.dmm = dmm
        self.comparator_lookup = comparator_lookup
        self.object_scoper = object_scoper

    @staticmethod
    def _lookup_comparison_operator(self, expression_operator):
        if str(expression_operator) not in self.comparator_lookup:
            raise NotImplementedError("Comparison operator {} unsupported for Splunk connector".format(expression_operator.name))
        return self.comparator_lookup[str(expression_operator)]

    def translate(self, expression):
        if isinstance(expression, ComparisonExpression):
            stix_object, stix_path = expression.object_path.split(':')

            # These are the native objects and fields
            object_mapping = self.dmm.map_object(stix_object)
            field_mapping = self.dmm.map_field(stix_object, stix_path)
            # This scopes the query to the object
            object_scoping = self.object_scoper(object_mapping)
            
            if stix_object == "x-readable-payload" and stix_path == "value":
                return "_raw=*{}*".format(expression.value)            
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
                self.comparator_lookup[str(expression.operator)],
                self.translate(expression.expr2)
            )

    def _field_severity(self, value):
        """
        check for severity and convert input value to
        informational,low,medium,high,critical
        param value
        return value(str)
        """
        value = int(value)
        if 1 <= value <= 20:
            value = "informational"
        elif 21 <= value <= 40:
            value = "low"
        elif 41 <= value <= 60:
            value = "medium"
        elif 61 <= value <= 80:
            value = "high"
        elif 81 <= value <= 100:
            value = "critical"
        else:
            raise NotImplementedError('only 1-100 integer values are supported with severity field')
        return value
        
    def _build_comparison(self, expression, object_scoping, field_mapping):
        comparator = self._lookup_comparison_operator(self, expression.comparator)
        if field_mapping == 'severity':
            expression.value = self._field_severity(expression.value)
        if isinstance(comparator, str):
            if comparator == "encoders.like":
                comparison = encoders.like(field_mapping, expression.value)
            elif comparator == "encoders.set":
                comparison = encoders.set(field_mapping, expression.value)
            elif comparator == "encoders.matches":
                comparison = encoders.matches(field_mapping, expression.value)
            elif comparator == "encoders.subset":
                comparison = encoders.subset(field_mapping, expression.value)
            else:
                comparison = "{} {} {}".format(
                    field_mapping,
                    comparator,
                    encoders.simple(expression.value)
                )
            splunk_comparison = self._maybe_negate(comparison, expression.negated)

            if isinstance(self.dmm, CarBaseQueryTranslator):
                return "({} AND {})".format(object_scoping, splunk_comparison)
            else:
                return "({})".format(splunk_comparison)
        else:
            return "({} AND {})".format(
                object_scoping,
                self._maybe_negate(comparator(field_mapping, expression.value), expression.negated)
            )

    def _maybe_negate(self, splunk_comparison, negated):
        if negated:
            return "NOT ({})".format(splunk_comparison)
        else:
            return splunk_comparison


def _test_for_earliest_latest(query_string) -> bool:
    pattern = r'(earliest="\d{2}/\d{2}/\d{4}:\d{2}:\d{2}:\d{2}")|(latest="\d{2}/\d{2}/\d{4}:\d{2}:\d{2}:\d{2}")'
    match = re.search(pattern, query_string)
    return bool(match)


def translate_pattern(pattern: Pattern, data_model_mapping, search_key, options):
    result_limit = options['result_limit']
    time_range = options['time_range']
    index = options.get('index')
    x = SplunkSearchTranslator(pattern, data_model_mapping, result_limit, time_range)
    translated_query = x.translate(pattern)
    has_earliest_latest = _test_for_earliest_latest(translated_query)

    # adding default fields for query

    map_data = data_model_mapping.select_fields["default"]
    fields = ""
    for field in map_data:
        if field != map_data[-1]:
            fields += field
            fields += ", "
        else:
            fields += field

    if index:
        indices = [i.strip(' ') for i in index.split(',')]
        index_cmd = ' OR '.join([f'index="{i}"' for i in indices])
        translated_query = f'{index_cmd} {translated_query}'

    if not has_earliest_latest:
        if _needs_where_command(translated_query):
            translated_query = 'earliest="{earliest}" | where {qry} | head {result_limit}'.format(qry=translated_query,
                                                                                                  earliest=time_range,
                                                                                                  result_limit=result_limit)
        else:
            translated_query += ' earliest="{earliest}" | head {result_limit}'.format(earliest=time_range, result_limit=result_limit)
    elif has_earliest_latest:
        translated_query += ' | head {result_limit}'.format(result_limit=result_limit)

    translated_query = search_key + " " + translated_query + " | fields {fields}".format(fields=fields)

    # return "({} AND {})".format(object_scoping, splunk_comparison)
    return translated_query
