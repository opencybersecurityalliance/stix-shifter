from stix_shifter_utils.stix_translation.src.patterns.pattern_objects import ObservationExpression, \
    ComparisonExpression, \
    ComparisonExpressionOperators, ComparisonComparators, Pattern, \
    CombinedComparisonExpression, CombinedObservationExpression, ObservationOperators, StartStopQualifier, SetValue
from datetime import datetime, timedelta
import os
import json

class SecuronixQueryStringPatternTranslator:
    """
    Translates STIX pattern into Securonix Spotter query format
    """
    QUERIES = []

    def __init__(self, pattern: Pattern, data_model_mapper, time_range):
        self.dmm = data_model_mapper
        self.comparator_lookup = self._load_comparator_mapping()
        self.pattern = pattern
        self.time_range = time_range
        self.translated = self.parse_expression(pattern)
        self.queries = []
        self.queries.extend(self.translated)

    def _load_comparator_mapping(self):
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(basepath, 'json', 'operators.json')
        with open(file_path, 'r') as f:
            return json.load(f)

    @staticmethod
    def _format_set(values) -> str:
        gen = values.element_iterator()
        return ','.join(str(value) for value in gen)

    @staticmethod
    def _escape_value(value, comparator=None) -> str:
        if isinstance(value, str):
            if comparator == "LIKE":
                value = value.replace('%', '*').replace('_', '?')
            elif comparator == "MATCHES":
                pass
            elif comparator == "CONTAINS":
                value = value.strip('%*')
            return f'"{value}"'
        elif isinstance(value, (int, float)):
            return str(value)
        else:
            return f'"{str(value)}"'

    @staticmethod
    def _format_datetime(timestamp_string):
        # Remove quotes and 't' prefix/suffix from timestamp
        cleaned = timestamp_string[2:-2]  # Removes t' and '
        if '.' in cleaned:
            cleaned = cleaned.split('.', 1)[0]
        dt = datetime.fromisoformat(cleaned.replace('Z', '+00:00'))
        return dt.strftime('%m/%d/%Y %H:%M:%S')

    def _format_start_stop_qualifier(self, expression: str, qualifier: StartStopQualifier) -> dict:
        """Returns a structured output with query and parameters"""
        start_time = self._format_datetime(qualifier.start)
        stop_time = self._format_datetime(qualifier.stop)
        
        return {
            'query': expression,
            'parameters': {
                'eventtime_from': start_time,
                'eventtime_to': stop_time
            }
        }

    def _parse_mapped_fields(self, value, comparator, mapped_fields_array) -> str:
        comparison_strings = []

        if isinstance(value, SetValue):
            value = self._format_set(value)
        
        if isinstance(value, str):
            if comparator == "LIKE" and value.strip('*?') == '':
                return " OR ".join(f"{field} NOT NULL" for field in mapped_fields_array)

        for mapped_field in mapped_fields_array:
            if comparator == "LIKE" and isinstance(value, str) and '*' in value:
                comparison_strings.append(f"{mapped_field} NOT NULL")
            else:
                if comparator == "IN":
                    comparison_strings.append(f"{mapped_field} IN ({value})")
                else:
                    escaped_value = self._escape_value(value, comparator)
                    comparison_strings.append(f"{mapped_field} {comparator} {escaped_value}")

        return f"({' OR '.join(comparison_strings)})" if comparison_strings else ""

    def _parse_expression(self, expression, qualifier=None) -> dict:
        if isinstance(expression, ComparisonExpression):  # Base Case
            # Map STIX Object and field to Securonix field
            stix_object, stix_field = expression.object_path.split(':')
            mapped_fields = self.dmm.map_field(stix_object, stix_field)
            
            if not mapped_fields:
                return {"query": "", "parameters": {}}

            # Get comparison operator 
            if expression.negated:
                if expression.comparator == ComparisonComparators.Equal:
                    comparator = "!="
                elif expression.comparator == ComparisonComparators.Like:
                    comparator = "NOT CONTAINS"
                else:
                    comparator = self._get_negate_comparator()
            else:
                # For non-negated LIKE comparator, handle wildcards
                if expression.comparator == ComparisonComparators.Like:
                    # Check if value exists and handle accordingly
                    if not hasattr(expression, 'value') or expression.value is None:
                        # Return a default query when value is missing or None
                        query_string = " OR ".join(f"{field} NOT NULL" for field in mapped_fields)
                        return {"query": query_string, "parameters": {}}
                        
                    if isinstance(expression.value, str):
                        if expression.value.strip('%') == '':
                            # Handle pure wildcard case - translate to NOT NULL
                            query_string = " OR ".join(f"{field} NOT NULL" for field in mapped_fields)
                            return {"query": query_string, "parameters": {}}
                        else:
                            comparator = "CONTAINS"  # Change from "LIKE"
                    else:
                        # Handle non-string value for LIKE comparator
                        comparator = "CONTAINS"
                else:
                    comparator = self.comparator_lookup.get(str(expression.comparator))
                    if not comparator:
                        raise RuntimeError(f"Unknown Comparison Operator: {expression.comparator}")

            query_string = self._parse_mapped_fields(expression.value, comparator, mapped_fields)
            return {"query": query_string, "parameters": {}}

        elif isinstance(expression, CombinedComparisonExpression):
            exp1 = self._parse_expression(expression.expr1)
            exp2 = self._parse_expression(expression.expr2)
            operator = self.comparator_lookup.get(str(expression.operator))

            if not operator:
                raise RuntimeError(f"Unknown Operator: {expression.operator}")

            # Handle cases where either expression might return None
            if not exp1 or not exp2:
                return {"query": "", "parameters": {}}

            query = f"({exp1.get('query', '')} {operator} {exp2.get('query', '')})"
            parameters = {**exp1.get('parameters', {}), **exp2.get('parameters', {})}
            return {"query": query, "parameters": parameters}

        elif isinstance(expression, ObservationExpression):
            result = self._parse_expression(expression.comparison_expression, qualifier)
            if result is None:
                return {"query": "", "parameters": {}}
            return result

        elif isinstance(expression, Pattern):
            if hasattr(expression, 'expression'):
                if isinstance(expression.expression, StartStopQualifier):
                    # First get the inner query from the observation expression
                    inner_result = self._parse_expression(expression.expression.observation_expression)
                    if inner_result is None:
                        inner_result = {"query": "", "parameters": {}}
                    # Then apply the time qualifier
                    return self._format_start_stop_qualifier(inner_result.get('query', ''), expression.expression)
                return self._parse_expression(expression.expression)

        elif isinstance(expression, StartStopQualifier):
            # Parse the observation expression with the qualifier
            result = self._parse_expression(expression.observation_expression)
            if result is None:
                result = {"query": "", "parameters": {}}
            return self._format_start_stop_qualifier(result.get("query", ""), expression)

        else:
            raise RuntimeError(f"Unknown expression type: {type(expression)}")

        # Default return to handle any other cases
        return {"query": "", "parameters": {}}
        
    def _format_start_stop_qualifier(self, expression: str, qualifier: StartStopQualifier) -> dict:
        """Returns a structured output with query and parameters"""
        # Remove the 't' prefix/suffix and quotes from timestamp
        start_time = qualifier.start.replace("t'", "").replace("'", "")
        stop_time = qualifier.stop.replace("t'", "").replace("'", "")
        
        # Convert to Securonix format
        start_dt = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
        stop_dt = datetime.fromisoformat(stop_time.replace('Z', '+00:00'))
        
        formatted_start = start_dt.strftime('%m/%d/%Y %H:%M:%S')
        formatted_stop = stop_dt.strftime('%m/%d/%Y %H:%M:%S')
        
        return {
            'query': expression if expression else "(sourceaddress NOT NULL OR destinationaddress NOT NULL)",
            'parameters': {
                'eventtime_from': formatted_start,
                'eventtime_to': formatted_stop
            }
        }

    def _get_negate_comparator(self):
        return self.comparator_lookup["ComparisonComparators.NotEqual"]

    def _add_default_timerange(self, query_struct: dict) -> dict:
        """Adds default time range if not already present"""
        if self.time_range and not query_struct.get('parameters', {}).get('eventtime_from'):
            current_time = datetime.now()
            start_time = current_time - timedelta(minutes=self.time_range)
            
            query_struct['parameters'].update({
                'eventtime_from': start_time.strftime('%m/%d/%Y %H:%M:%S'),
                'eventtime_to': current_time.strftime('%m/%d/%Y %H:%M:%S')
            })
        
        return query_struct

    def parse_expression(self, pattern: Pattern):
        """Main entry point for parsing"""
        query_struct = self._parse_expression(pattern)
        if query_struct is None:
            query_struct = {"query": "", "parameters": {}}
        return self._add_default_timerange(query_struct)


def translate_pattern(pattern: Pattern, data_model_mapping, options):
    """
    Translates STIX pattern into Securonix query format
    Returns a dictionary containing the query and parameters
    """
    time_range = options.get('time_range', None)

    # Initialize translator with pattern
    translator = SecuronixQueryStringPatternTranslator(pattern, data_model_mapping, time_range)
    
    # Get the translated query
    query_struct = translator.translated

    return query_struct
