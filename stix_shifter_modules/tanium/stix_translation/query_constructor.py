import regex
from stix_shifter_modules.tanium.stix_translation.transformers import ConvertTextSeverityToNumberValue
from stix_shifter_utils.stix_translation.src.patterns.pattern_objects import ObservationExpression, ComparisonExpression, \
    Pattern,\
    CombinedComparisonExpression, CombinedObservationExpression
from stix_shifter_utils.stix_translation.src.utils.transformers import TimestampToMilliseconds
import logging

TIMESTAMP_STIX_PROPERTIES = ["created", "modified", "accessed", "ctime", "mtime", "atime", "created_time", "modifed_time"]

logger = logging.getLogger(__name__)

class QueryStringPatternTranslator:

    def __init__(self, pattern: Pattern, data_model_mapper):
        self.fieldList = []
        self.dmm = data_model_mapper
        self.comparator_lookup = self.dmm.map_comparator()
        self.pattern = pattern
        self.observation_query_list = []
        self.translated = self.parse_expression(pattern)

    @classmethod
    def _format_start_stop_qualifier(self, expression, qualifier) -> str:
        """Convert a STIX start stop qualifier into a query string."""
        qualifier_split = qualifier.split("'")
        start = qualifier_split[1]
        stop = qualifier_split[3]
        qualified_query = f"{expression}&alertedAtFrom={start}&alertedAtUntil={stop}"
        return qualified_query
    
    @staticmethod
    def _format_severity(self, value):
        if(value < 40):
            return "info"
        elif(value >= 40 and value < 80):
            return "low"
        elif(value >= 80):
            return "high"

    @staticmethod
    def _parse_mapped_fields(self, value, comparator, mapped_fields_array):
        if(mapped_fields_array[0] == "severity"):
            value = QueryStringPatternTranslator._format_severity(self, value)
        parsed_fields = f"{mapped_fields_array[0]}{comparator}{value}"

        if(comparator == "IN"):
            parsed_fields = ""
            for current_value in value.values:
                if(mapped_fields_array[0] == "severity"):
                    value = QueryStringPatternTranslator._format_severity(self, value)
                parsed_fields += f"{mapped_fields_array[0]}={current_value}&"
            parsed_fields = parsed_fields[:-1]
        return parsed_fields

    @staticmethod
    def _lookup_comparison_operator(self, expression_operator):
        if str(expression_operator) not in self.comparator_lookup:
            raise NotImplementedError(f"Comparison operator {expression_operator.name} unsupported for Tanium connector")
        return self.comparator_lookup[str(expression_operator)]

    def _parse_expression(self, expression, qualifier=None) -> str:
        if isinstance(expression, ComparisonExpression):  # Base Case
            # Resolve STIX Object Path to a field in the target Data Model
            stix_object, stix_field = expression.object_path.split(':')
            # Multiple data source fields may map to the same STIX Object
            mapped_fields_array = self.dmm.map_field(stix_object, stix_field)
            # Resolve the comparison symbol to use in the query string (usually just ':')
            comparator = self._lookup_comparison_operator(self, expression.comparator)
            comparison_string = self._parse_mapped_fields(self, expression.value, comparator, mapped_fields_array)

            if qualifier:
                comparison_string = self._format_start_stop_qualifier(comparison_string, qualifier)
                return comparison_string
            else:
                return f"{comparison_string}"
        elif isinstance(expression, CombinedComparisonExpression):
            operator = self._lookup_comparison_operator(self, expression.operator)
            expression_01 = self._parse_expression(expression.expr1)
            expression_02 = self._parse_expression(expression.expr2)
                
            self.validate_comparison_expression_operators(expression_01, expression_02, expression.operator)
            
            if not expression_01 or not expression_02:
                return ''
            query_string = f"{expression_02}{operator}{expression_01}"
            if qualifier:
                query_string = self._format_start_stop_qualifier(query_string, qualifier)
                return query_string
            else:
                return f"{query_string}"
        elif isinstance(expression, ObservationExpression):
            self.observation_query_list.append(self._parse_expression(expression.comparison_expression, qualifier))
            self.fieldList = []
        elif hasattr(expression, 'qualifier') and hasattr(expression, 'observation_expression'):
            if isinstance(expression.observation_expression, CombinedObservationExpression):
                operator = self._lookup_comparison_operator(self, expression.observation_expression.operator)
                observation_1 = self._parse_expression(expression.observation_expression.expr1)
                self.fieldList = []
                observation_2 = self._parse_expression(expression.observation_expression.expr2, expression.qualifier)
                self.fieldList = []           
                self.observation_query_list.append(observation_1)
                self.observation_query_list.append(observation_2)
            else:
                observation_1 = self._parse_expression(expression.observation_expression.comparison_expression, expression.qualifier)
                self.fieldList = []
                self.observation_query_list.append(observation_1)
                
        elif isinstance(expression, CombinedObservationExpression):
            operator = self._lookup_comparison_operator(self, expression.operator)
            observation_1 = self._parse_expression(expression.expr1)
            self.fieldList = []
            observation_2 = self._parse_expression(expression.expr2)
            self.fieldList = []
            
            if observation_1:
                self.observation_query_list.append(observation_1)
            if observation_2:
                self.observation_query_list.append(observation_2)
        elif isinstance(expression, Pattern):
            return f"{self._parse_expression(expression.expression)}"
        else:
            raise RuntimeError(f"Unknown Recursion Case for expression={expression}, type(expression)={type(expression)}")
        
    def parse_expression(self, pattern: Pattern):
        self._parse_expression(pattern)
        return self.observation_query_list
        
    def validate_comparison_expression_operators(self, expression_01, expression_02, operator):
        field1 = regex.split("=|&", expression_01)
        field2 = regex.split("=|&", expression_02)
        
        #The logic for comparison queries is AND Followed by OR. 
        if(operator.name == "And"):
            if(len(field1) == 2 and len(field2) == 2):
                if(field1[0] == field2[0]):
                    raise RuntimeError(f"The translation is not valid as this API does not support AND queries between the same field.")
            if(field1[0] not in self.fieldList):
                self.fieldList.append(field1[0])
                return True
            else:
                raise RuntimeError(f"The translation is not valid as this API does not support AND queries between the same field.")
            
        if(operator.name == "Or"):
            for index1 in range(0, len(field1) - 1,  +2):
                for index2 in range(0, len(field2) - 1,  +2):
                    if(field1[index1] != field2[index2]):
                        raise RuntimeError(f"The translation is not valid as this API does not support OR queries between different fields.")

def translate_pattern(pattern: Pattern, data_model_mapping, options):
    try:
        observation_query_list = QueryStringPatternTranslator(pattern, data_model_mapping).translated
    except Exception as err:
        raise err
    
    return observation_query_list
