from stix_shifter_utils.stix_translation.src.patterns.pattern_objects import ObservationExpression, ComparisonExpression, \
    ComparisonExpressionOperators, ComparisonComparators, Pattern, \
    CombinedComparisonExpression, CombinedObservationExpression, ObservationOperators, StartStopQualifier
from stix_shifter_utils.stix_translation.src.utils.transformers import TimestampToMilliseconds
from stix_shifter_utils.stix_translation.src.json_to_stix import observable
import logging
import re
from collections import defaultdict
from datetime import datetime
import calendar
import json

# Source and destination reference mapping for ip and mac addresses.
# Change the keys to match the data source fields. The value array indicates the possible data type that can come into from field.
REFERENCE_DATA_TYPES = {"srcip": ["ipv4", "ipv4_cidr"],
                        "srcipv6": ["ipv6"],
                        "dstip": ["ipv4", "ipv4_cidr"],
                        "dstipv6": ["ipv6"]}

logger = logging.getLogger(__name__)


class QueryStringPatternTranslator:

    def __init__(self, pattern: Pattern, data_model_mapper):
        self.dmm = data_model_mapper
        self.comparator_lookup = self.dmm.map_comparator()
        self.pattern = pattern
        self.index_queries = defaultdict(list)  # Store queries by index
        self.time_range = None  # Store START and STOP times
        self.parse_expression(pattern)

    @staticmethod
    def _format_set(values) -> str:
        gen = values.element_iterator()
        formatted_values = [QueryStringPatternTranslator._escape_value(value) for value in gen]
        return "({})".format(' OR '.join(formatted_values))

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
        return "{}".format(raw)

    @staticmethod
    def _format_equality(value) -> str:
        return '{}'.format(value)

    @staticmethod
    def _format_like(value) -> str:
        value = "*{}*".format(value)
        return QueryStringPatternTranslator._escape_value(value)

    @staticmethod
    def _escape_value(value, comparator=None) -> str:
        if isinstance(value, str):
            # For StellarCyber, escape only necessary characters
            return '{}'.format(value.replace('\\', '\\\\').replace('"', '\\"'))
        else:
            return value

    @staticmethod
    def _negate_comparison(comparison_string):
        return "NOT {}".format(comparison_string)

    @staticmethod
    def _check_value_type(value):
        value = str(value)
        for key, pattern in observable.REGEX.items():
            if key != 'date' and bool(re.search(pattern, value)):
                return key
        return None

    @staticmethod
    def _get_index_and_field(mapped_field):
        """Extract index and field name"""
        if '.' in mapped_field:
            index, field = mapped_field.split('.', 1)
            return index, field
        return None, mapped_field

    @staticmethod
    def _get_stellar_comparator(comparator, expression=None):
        """
        Converts STIX comparators to StellarCyber format
        For equality, always use ':'
        """
        if expression and (expression.comparator == ComparisonComparators.Equal or 
                          expression.comparator == ComparisonComparators.NotEqual):
            return ":"
        return comparator

    @staticmethod
    def _datetime_to_epoch_millis(datetime_str):
        """Convert ISO 8601 datetime string to milliseconds since epoch"""
        try:
            # Parse ISO 8601 date format
            dt = datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%S.%fZ")
        except ValueError:
            # Try without fractional seconds
            dt = datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%SZ")
        
        # Convert to milliseconds since epoch
        return int(calendar.timegm(dt.timetuple()) * 1000 + dt.microsecond / 1000)

    def _extract_timestamp_qualifier(self, qualifier):
        """Extract START and STOP times from qualifier and convert to milliseconds since epoch"""
        if not qualifier:
            return None
        
        # Match the datetime strings in the qualifier
        timestamp_pattern = r"t'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z)'"
        timestamps = re.findall(timestamp_pattern, qualifier)
        
        if len(timestamps) != 2:
            return None
        
        start_time = self._datetime_to_epoch_millis(timestamps[0])
        stop_time = self._datetime_to_epoch_millis(timestamps[1])
        
        return {
            'start': start_time,
            'stop': stop_time
        }

    def _parse_expression(self, expression, qualifier=None):
        """
        Parse the STIX expression and organize queries by index
        Returns a dict of index -> query mappings
        """
        # Check for timestamp qualifiers first
        if isinstance(expression, StartStopQualifier):
            self.time_range = self._extract_timestamp_qualifier(expression.qualifier)
            return self._parse_expression(expression.observation_expression, expression.qualifier)
            
        # For other expression types, continue with normal processing
        result = {}
        
        if isinstance(expression, ComparisonExpression):  # Base Case
            # Resolve STIX Object Path to a field in the target Data Model
            stix_object, stix_field = expression.object_path.split(':')
            # Multiple data source fields may map to the same STIX Object
            mapped_fields_array = self.dmm.map_field(stix_object, stix_field)
            # Resolve the comparison symbol to use in the query string
            comparator = self._lookup_comparison_operator(self, expression.comparator)
            
            # Format values based on the comparison type
            if stix_field == 'start' or stix_field == 'end':
                transformer = TimestampToMilliseconds()
                expression.value = transformer.transform(expression.value)

            if expression.comparator == ComparisonComparators.Matches:
                value = self._format_match(expression.value)
            elif expression.comparator == ComparisonComparators.In:
                value = self._format_set(expression.value)
            elif expression.comparator == ComparisonComparators.Equal or expression.comparator == ComparisonComparators.NotEqual:
                value = self._format_equality(expression.value)
            elif expression.comparator == ComparisonComparators.Like:
                value = self._format_like(expression.value)
            else:
                value = self._escape_value(expression.value)
                
            # Group fields by index
            fields_by_index = defaultdict(list)
            for mapped_field in mapped_fields_array:
                index, field = self._get_index_and_field(mapped_field)
                if index:
                    fields_by_index[index].append(field)
            
            # Create query parts for each index
            for index, fields in fields_by_index.items():
                query_parts = []
                stellar_comparator = self._get_stellar_comparator(comparator, expression)
                
                for field in fields:
                    query_part = "{}{}{}".format(field, stellar_comparator, value)
                    query_parts.append(query_part)
                
                if len(query_parts) == 1:
                    query_str = query_parts[0]
                else:
                    query_str = "(" + " OR ".join(query_parts) + ")"
                
                if expression.negated:
                    query_str = self._negate_comparison(query_str)
                
                result[index] = query_str
            
            return result
            
        elif isinstance(expression, CombinedComparisonExpression):
            operator = self._lookup_comparison_operator(self, expression.operator)
            expr1_result = self._parse_expression(expression.expr1)
            expr2_result = self._parse_expression(expression.expr2)
            
            # Combine results from both expressions
            all_indices = set(list(expr1_result.keys()) + list(expr2_result.keys()))
            
            for index in all_indices:
                # Get expressions for this index from both sides (if they exist)
                expr1_part = expr1_result.get(index)
                expr2_part = expr2_result.get(index)
                
                # Skip if neither expression exists for this index
                if not expr1_part and not expr2_part:
                    continue
                
                # Handle cases where one side might not have this index
                if expr1_part and expr2_part:
                    # Need to wrap in parentheses if they're complex expressions
                    if isinstance(expression.expr1, CombinedComparisonExpression):
                        expr1_part = "({})".format(expr1_part)
                    if isinstance(expression.expr2, CombinedComparisonExpression):
                        expr2_part = "({})".format(expr2_part)
                    
                    combined = "{} {} {}".format(expr1_part, operator, expr2_part)
                    result[index] = combined
                elif expr1_part:
                    result[index] = expr1_part
                elif expr2_part:
                    result[index] = expr2_part
            
            return result
            
        elif isinstance(expression, ObservationExpression):
            return self._parse_expression(expression.comparison_expression, qualifier)
            
        elif hasattr(expression, 'qualifier') and hasattr(expression, 'observation_expression'):
            # Handle StartStopQualifier cases
            if hasattr(expression, 'start') and hasattr(expression, 'stop'):
                self.time_range = self._extract_timestamp_qualifier(expression.qualifier)
            
            if isinstance(expression.observation_expression, CombinedObservationExpression):
                operator = self._lookup_comparison_operator(self, expression.observation_expression.operator)
                expr1_result = self._parse_expression(expression.observation_expression.expr1)
                expr2_result = self._parse_expression(expression.observation_expression.expr2, expression.qualifier)
                
                # Combine results with the proper operator
                all_indices = set(list(expr1_result.keys()) + list(expr2_result.keys()))
                
                for index in all_indices:
                    expr1_part = expr1_result.get(index)
                    expr2_part = expr2_result.get(index)
                    
                    if expr1_part and expr2_part:
                        result[index] = "{} {} {}".format(expr1_part, operator, expr2_part)
                    elif expr1_part:
                        result[index] = expr1_part
                    elif expr2_part:
                        result[index] = expr2_part
                
                return result
            else:
                return self._parse_expression(expression.observation_expression.comparison_expression, expression.qualifier)
                
        elif isinstance(expression, CombinedObservationExpression):
            operator = self._lookup_comparison_operator(self, expression.operator)
            expr1_result = self._parse_expression(expression.expr1)
            expr2_result = self._parse_expression(expression.expr2)
            
            # Combine results from both expressions
            all_indices = set(list(expr1_result.keys()) + list(expr2_result.keys()))
            
            for index in all_indices:
                expr1_part = expr1_result.get(index)
                expr2_part = expr2_result.get(index)
                
                if expr1_part and expr2_part:
                    result[index] = "({}) {} ({})".format(expr1_part, operator, expr2_part)
                elif expr1_part:
                    result[index] = expr1_part
                elif expr2_part:
                    result[index] = expr2_part
            
            return result
            
        elif isinstance(expression, Pattern):
            return self._parse_expression(expression.expression)
            
        else:
            raise RuntimeError("Unknown Recursion Case for expression={}, type(expression)={}".format(
                expression, type(expression)))

    @staticmethod
    def _is_reference_value(stix_field):
        return stix_field == 'src_ref.value' or stix_field == 'dst_ref.value'

    @staticmethod
    def _lookup_comparison_operator(self, expression_operator):
        if str(expression_operator) not in self.comparator_lookup:
            raise NotImplementedError("Comparison operator {} unsupported for connector".format(expression_operator.name))
        return self.comparator_lookup.get(str(expression_operator))

    def parse_expression(self, pattern: Pattern):
        """
        Parse the pattern and store queries by index
        """
        index_queries = self._parse_expression(pattern)
        self.index_queries = index_queries
        return index_queries

    def add_time_range_to_queries(self, index_queries):
        """Add time range constraints to all queries if time_range is available"""
        if not self.time_range:
            return index_queries
            
        # For each index, append the timestamp range constraint
        for index, query in index_queries.items():
            time_constraint = " AND timestamp:[{} TO {}]".format(
                self.time_range['start'], 
                self.time_range['stop']
            )
            
            # Add parentheses around the original query if needed
            if " AND " in query or " OR " in query:
                if not (query.startswith("(") and query.endswith(")")):
                    index_queries[index] = "(" + query + ")" + time_constraint
                else:
                    index_queries[index] = query + time_constraint
            else:
                index_queries[index] = query + time_constraint
                
        return index_queries


def translate_pattern(pattern: Pattern, data_model_mapping, options):
    # Query result limit and time range can be passed into the QueryStringPatternTranslator if supported by the data source.
    # result_limit = options['result_limit']
    # time_range = options['time_range']

    print("pattern: ", pattern)
    translator = QueryStringPatternTranslator(pattern, data_model_mapping)
    index_queries = translator.parse_expression(pattern)
    
    # Add time range constraints if present in the pattern
    index_queries = translator.add_time_range_to_queries(index_queries)
    
    # Process START STOP qualifiers in each query
    for index, query in index_queries.items():
        index_queries[index] = query.replace("START ", "").replace(" STOP ", "")
    
    # Format output as {index1: [queries1], index2: [queries2], ...}
    queries = []
    for index, query in index_queries.items():
        queries.append("index={}&{}".format(index, query))
    return queries
