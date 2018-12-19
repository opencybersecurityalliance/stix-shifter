from stix_shifter.stix_translation.src.patterns.pattern_objects import ObservationExpression, ComparisonExpression, \
    ComparisonExpressionOperators, ComparisonComparators, Pattern, \
    CombinedComparisonExpression, CombinedObservationExpression, ObservationOperators
from stix_shifter.stix_translation.src.patterns.errors import SearchFeatureNotSupportedError


class RelevanceQueryStringPatternTranslator:
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
        ComparisonComparators.Matches: 'MATCHES',
        ComparisonComparators.IsSubSet: 'INCIDR',
        ObservationOperators.Or: 'OR',
        # Treat AND's as OR's -- Unsure how two ObsExps wouldn't cancel each other out.
        ObservationOperators.And: 'OR'
    }

    query_types = {
        "file": "file",
        "process": "process"
    }

    query_format = {
        "file_name_path": "(name of it | \"n/a\", \"sha256\", sha256 of it | \"n/a\", pathname of it | \"n/a\") of files of folder (\"{expr2_value}\")",        
        "file_hash_path": "(name of it | \"n/a\", \"sha256\", sha256 of it | \"n/a\", pathname of it | \"n/a\") of files whose ({stix_object} of it as lowercase contains \"{expr1_value}\" as lowercase) of folder (\"{expr2_value}\")",
        "file_name_hash_path": "(name of it | \"n/a\", \"sha256\", sha256 of it | \"n/a\", pathname of it | \"n/a\") of files whose ({name_object} of it as lowercase contains \"{expr1_value}\" as lowercase AND {sha265_object} of it as lowercase = \"{expr3_value}\" as lowercase) of folder (\"{expr2_value}\")",
        "processes": "( name of it | \"n/a\", process id of it as string | \"n/a\", \"sha256\", sha256 of image file of it | \"n/a\", pathname of image file of it | \"n/a\" ) of processes whose ({stix_object} of it as lowercase contains \"{expr1_value}\" as lowercase )",
        "process_name_hash": "( name of it | \"n/a\", process id of it as string | \"n/a\", \"sha256\", sha256 of image file of it | \"n/a\", pathname of image file of it | \"n/a\" ) of processes whose ({stix_object1} of it as lowercase contains \"{expr1_value}\" as lowercase {comparator} {stix_object2} of image file of it as lowercase = \"{expr2_value}\" as lowercase )"
    }

    query_string = {}
    query_type = ""

    def __init__(self, pattern: Pattern, data_model_mapper, result_limit):
        self.dmm = data_model_mapper
        self.pattern = pattern
        self.result_limit = result_limit
        self.translated = self.parse_expression(pattern)
        self.queries = self.translated
        
    
    @staticmethod
    def _escape_value(value, comparator=None) -> str:
        if isinstance(value, str):
            return '{}'.format(value.replace('\\', '\\\\').replace('\"', '\\"').replace('(', '\\(').replace(')', '\\)'))
        else:
            return value
    
    def _parse_expression(self, expression, qualifier=None):
        if isinstance(expression, ComparisonExpression):  # Base Case
             # Resolve STIX Object Path to a field in the target Data Model
            stix_object, stix_remainings = expression.object_path.split(':')
            value = self._escape_value(expression.value)
            # comparator = self.comparator_lookup[expression.comparator]
            stix_property = ""
            stix_key = ""
            self.query_type = stix_object

            if '.' in stix_remainings:
                stix_property_and_key = stix_remainings.split('.')
                stix_property = stix_property_and_key[0]
                stix_key = stix_property_and_key[1]

            if stix_remainings == 'parent_directory_ref.path':
                reference_property = 'folder'
            else:
                if stix_key != "":
                    reference_property = stix_key
                else:
                    reference_property = stix_remainings
            
            self.query_string.update({reference_property:value})
            self.query_string.update({'query_type':self.query_type})

            return self.query_string
        elif isinstance(expression, CombinedComparisonExpression):
            self._parse_expression(expression.expr1)
            comparator = self.comparator_lookup[expression.operator]
            self._parse_expression(expression.expr2)

            self.query_string.update({'comparator':comparator})

            if qualifier is not None:
                return "SPLIT{} limit {} {}SPLIT".format(self.query_string, self.result_limit, qualifier)
            else:
                return self.query_string
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
            return "{expr1} {operator} {expr2}".format(expr1=self._parse_expression(expression.expr1),
                                                       operator=operator,
                                                       expr2=self._parse_expression(expression.expr2))
        elif isinstance(expression, Pattern):
            return self._parse_expression(expression.expression)
        else:
            raise RuntimeError("Unknown Recursion Case for expression={}, type(expression)={}".format(
                expression, type(expression)))

    def parse_expression(self, pattern: Pattern):
        return self._parse_expression(pattern)
    
def translate_pattern(pattern: Pattern, data_model_mapping, result_limit, timerange=None):
    statements = {}
    translated_statements = RelevanceQueryStringPatternTranslator(pattern, data_model_mapping, result_limit)
    statements = translated_statements.queries
    query_type = statements.get('query_type')
    format_type = ""
    final_query = ""
    name_object = 'name'
    sha265_object = 'sha256'

    if query_type == 'file':
        if sha265_object not in statements:
            file_name = statements.get('name')
            path_value = statements.get('folder')
            if file_name != "*":
                format_type = 'file_hash_path'
                final_query = RelevanceQueryStringPatternTranslator.query_format.get(format_type).format(stix_object=name_object,expr1_value=file_name,expr2_value=path_value)
            else:
                format_type = 'file_name_path'
                final_query = RelevanceQueryStringPatternTranslator.query_format.get(format_type).format(expr2_value=path_value)
        elif name_object not in statements:
            hash_value = statements.get('sha256')
            path_name = statements.get('folder')
            format_type = 'file_hash_path'
            final_query = RelevanceQueryStringPatternTranslator.query_format.get(format_type).format(stix_object=sha265_object,expr1_value=hash_value,expr2_value=path_name)
        elif name_object in statements and 'sha256' in statements and 'folder' in statements:
            file_name = statements.get('name')
            path_name = statements.get('folder')
            hash_value = statements.get('sha256')
            format_type = 'file_name_hash_path'
            final_query = RelevanceQueryStringPatternTranslator.query_format.get(format_type).format(name_object=name_object,expr1_value=file_name,sha265_object=sha265_object,expr3_value=hash_value,expr2_value=path_name)
    elif query_type == 'process':
        if sha265_object not in statements:
            file_name = statements.get('name')
            format_type = 'processes'
            final_query = RelevanceQueryStringPatternTranslator.query_format.get(format_type).format(stix_object=name_object,expr1_value=file_name)
        else:
            file_name = statements.get('name')
            hash_value = statements.get('sha256')
            format_type = 'process_name_hash'
            final_query = RelevanceQueryStringPatternTranslator.query_format.get(format_type).format(stix_object1=name_object,expr1_value=file_name,comparator=statements.get('comparator'), stix_object2=sha265_object,expr2_value=hash_value)
    else:
        print('Undefined query type')

    return final_query