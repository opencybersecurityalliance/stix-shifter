import logging
import datetime
import json

logger = logging.getLogger(__name__)

from stix2patterns_translator.pattern_objects import ObservationExpression, ComparisonExpression, \
    ComparisonExpressionOperators, ComparisonComparators, Pattern, \
    CombinedComparisonExpression, CombinedObservationExpression, ObservationOperators
from stix2patterns_translator.errors import SearchFeatureNotSupportedError
from stix_shifter.src.transformers import TimestampToEpoch, ValueTransformer

class DataMappingException(Exception):
    pass

class MongoQueryStringPatternTranslator:
    comparator_lookup = {
        ComparisonExpressionOperators.And: "$and",
        ComparisonExpressionOperators.Or: "$or",
        ComparisonComparators.GreaterThan: "$gt",
        ComparisonComparators.GreaterThanOrEqual: "$gte",
        ComparisonComparators.LessThan: "$lt",
        ComparisonComparators.LessThanOrEqual: "$lte",
        ComparisonComparators.Equal: "$eq",
        ComparisonComparators.NotEqual: "$ne",
        ComparisonComparators.Like: "$regex", # Will be ugly
        ComparisonComparators.In: "$in", # 
        ComparisonComparators.Matches: '$regex',  # Will be ugly
        ObservationOperators.Or: '$or',
        # Treat AND's as OR's -- Unsure how two ObsExps wouldn't cancel each other out.
        ObservationOperators.And: '$and'
    }
    def __init__(self, pattern: Pattern, data_model_mapper):
        self.dmm = data_model_mapper
        self.pattern = pattern
        self.translated = self.parse_expression(pattern)
    @staticmethod
    def _format_equality(value) -> str:
        return value
    @staticmethod
    def _format_like(value) -> str:
        # Convert '.' to r'\.'
        # Convert r'%' to r'.*'
        # Convvert r'_' to r'.'
        value = value.replace('.', r'\.').replace('%', '.*').replace('_', '.')
        # Wrap in ^$?
        return '/%s/' % value
    @staticmethod
    def _format_match(value) -> str:
        raw = value
        if raw[0] == "^":
            raw = raw[1:]
        else:
            raw = ".*" + raw
        if raw[-1] == "$":
            raw = raw[0:-1]
        else:
            raw = raw + ".*"
        return '/%s/' % raw
    @staticmethod
    def _format_set(values) -> list:
        gen = values.element_iterator()
        return [x for x in gen]
    def _parse_expression(self, expression) -> dict:
        print(expression)
        if isinstance(expression, ComparisonExpression):  # Base Case
            stix_object, stix_field = expression.object_path.split(':')
            # Determine what objects these should map to based on type
            # configure from json
            mapped_fields_array = self.dmm.map_field(stix_object, stix_field)
            # What was the comparison
            comparator = self.comparator_lookup[expression.comparator]
            # First is a value transformation
            if stix_field == 'protocols[*]':
                return "Not Implemented"
            elif stix_field == 'start' or stix_field == 'end':
                transformer = TimestampToEpoch()
                expression.value = transformer.transform(expression.value)
            if expression.comparator == ComparisonComparators.Matches:
                value = self._format_match(expression.value)
            elif expression.comparator == ComparisonComparators.In:
                value = self._format_set(expression.value)
            elif expression.comparator == ComparisonComparators.Equal or expression.comparator == ComparisonComparators.NotEqual:
                value = self._format_equality(expression.value)
                logger.debug("Equality of Not Equality")
            elif expression.comparator == ComparisonComparators.Like:
                value = self._format_like(expression.value)
            else:
                value = stix_object
            # Next we convert what we have into the Mongo Query
            if len(mapped_fields_array) > 1:
                expression = {"$or" : [{mapped_field : {comparator : value}} for mapped_field in mapped_fields_array]}
            elif len(mapped_fields_array) == 1:
                expression = {mapped_fields_array[0] : {comparator : value}}
            else:
                raise DataMappingException("Fields have no known mapping into Mongo Schema Provided")
            # And return
            return expression
        elif isinstance(expression, CombinedComparisonExpression):
            return {
                self.comparator_lookup[expression.operator] : [
                    self._parse_expression(expression.expr1),
                    self._parse_expression(expression.expr2)
                ]
            }
        elif isinstance(expression, ObservationExpression):
            return self._parse_expression(expression.comparison_expression)
        elif isinstance(expression, CombinedObservationExpression):
            return {
                self.comparator_lookup[expression.operator] : [
                    self._parse_expression(expression.expr1),
                    self._parse_expression(expression.expr2)
                ]
            }
        elif isinstance(expression, Pattern):
            return self._parse_expression(expression.expression)
        else:
            raise RuntimeError("Unknown Recursion Case for expression={}, type(expression)={}".format(
                expression, type(expression)))
    def parse_expression(self, pattern: Pattern):
        return self._parse_expression(pattern)


def translate_pattern(pattern: Pattern, data_model_mapping):
    x = MongoQueryStringPatternTranslator(pattern, data_model_mapping)
    return x.translated
