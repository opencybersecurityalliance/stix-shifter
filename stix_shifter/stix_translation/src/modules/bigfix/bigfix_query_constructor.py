from stix_shifter.stix_translation.src.patterns.pattern_objects import ObservationExpression, ComparisonExpression, \
    ComparisonExpressionOperators, ComparisonComparators, Pattern, \
    CombinedComparisonExpression, CombinedObservationExpression, ObservationOperators
from stix_shifter.stix_translation.src.patterns.errors import SearchFeatureNotSupportedError


class RelevanceQueryStringPatternTranslator:
    comparator_lookup = {
        ComparisonExpressionOperators.And: "AND",
        ComparisonExpressionOperators.Or: "OR",
        # ComparisonComparators.GreaterThan: ">",
        # ComparisonComparators.GreaterThanOrEqual: ">=",
        # ComparisonComparators.LessThan: "<",
        # ComparisonComparators.LessThanOrEqual: "<=",
        ComparisonComparators.Equal: "=",
        ComparisonComparators.NotEqual: "!=",
        ComparisonComparators.Like: "contains",
        # ComparisonComparators.In: "IN",
        ComparisonComparators.Matches: 'MATCHES',
        # ComparisonComparators.IsSubSet: 'INCIDR',
        ObservationOperators.Or: 'OR',
        # Treat AND's as OR's -- Unsure how two ObsExps wouldn't cancel each other out.
        ObservationOperators.And: 'OR'
    }

    query_types = {
        "file": "file",
        "process": "process"
    }

    query_format = {
        "all_files_in_directory": "(\"file\", name of it | \"n/a\", \"sha256\", sha256 of it | \"n/a\", \"sha1\", sha1 of it | \"n/a\", \"md5\", md5 of it | \"n/a\", pathname of it | \"n/a\", (modification time of it - \"01 Jan 1970 00:00:00 +0000\" as time)/second ) of files of folder (\"{file_path}\")",        
        "file_query": "(\"file\", name of it | \"n/a\", \"sha256\", sha256 of it | \"n/a\", \"sha1\", sha1 of it | \"n/a\", \"md5\", md5 of it | \"n/a\", pathname of it | \"n/a\", (modification time of it - \"01 Jan 1970 00:00:00 +0000\" as time)/second ) of files whose ({stix_object} of it as lowercase {object_value} as lowercase) of folder (\"{file_path}\")",
        "file_name_with_hash": "(\"file\", name of it | \"n/a\", \"sha256\", sha256 of it | \"n/a\", \"sha1\", sha1 of it | \"n/a\", \"md5\", md5 of it | \"n/a\", pathname of it | \"n/a\", (modification time of it - \"01 Jan 1970 00:00:00 +0000\" as time)/second ) of files whose ({name_object} of it as lowercase {file_name} as lowercase {expression_operator} {hash_type} of it as lowercase {hash_value} as lowercase) of folder (\"{file_path}\")",
        "all_processes": "( \"process\", name of it | \"n/a\", process id of it as string | \"n/a\", \"sha256\", sha256 of image file of it | \"n/a\", \"sha1\", sha1 of image file of it | \"n/a\", \"md5\", md5 of image file of it | \"n/a\", pathname of image file of it | \"n/a\", (start time of it - \"01 Jan 1970 00:00:00 +0000\" as time)/second ) of processes",
        "filter_processes_with_name": "( \"process\", name of it | \"n/a\", process id of it as string | \"n/a\", \"sha256\", sha256 of image file of it | \"n/a\", \"sha1\", sha1 of image file of it | \"n/a\", \"md5\", md5 of image file of it | \"n/a\", pathname of image file of it | \"n/a\", (start time of it - \"01 Jan 1970 00:00:00 +0000\" as time)/second ) of processes whose ({process_object} of it as lowercase {process_name} as lowercase )",
        "process_name_with_hash": "( \"process\", name of it | \"n/a\", process id of it as string | \"n/a\", \"sha256\", sha256 of image file of it | \"n/a\", \"sha1\", sha1 of image file of it | \"n/a\", \"md5\", md5 of image file of it | \"n/a\", pathname of image file of it | \"n/a\", (start time of it - \"01 Jan 1970 00:00:00 +0000\" as time)/second ) of processes whose ({process_object} of it as lowercase {process_name} as lowercase {expression_operator} {hash_type} of image file of it as lowercase {hash_value} as lowercase )"
    }

    query_string = {}
    query_type = ""

    def __init__(self, pattern: Pattern, result_limit):
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
            comparator = self.comparator_lookup[expression.comparator]
            final_value = comparator + ' "' + value + '"'
            stix_property = ""
            stix_key = ""
            self.query_type = stix_object

            if '.' in stix_remainings:
                stix_property_and_key = stix_remainings.split('.')
                stix_property = stix_property_and_key[0]
                stix_key = stix_property_and_key[1]

            if stix_remainings == 'parent_directory_ref.path':
                reference_property = 'folder'
                self.query_string.update({reference_property:value})
            else:
                if stix_key != "":
                    reference_property = stix_key
                    self.query_string.update({stix_property:stix_key})
                    self.query_string.update({'value':final_value})
                else:
                    reference_property = stix_remainings
                    self.query_string.update({reference_property:final_value})

            self.query_string.update({'query_type':self.query_type})
            self.query_string.update({'comparator':comparator})

            return self.query_string
        elif isinstance(expression, CombinedComparisonExpression):
            self._parse_expression(expression.expr1)
            expression_operator = self.comparator_lookup[expression.operator]
            self._parse_expression(expression.expr2)

            self.query_string.update({'expression_operator':expression_operator})

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
    
def translate_pattern(pattern: Pattern, result_limit, timerange=None):
    statements = {}
    translated_statements = RelevanceQueryStringPatternTranslator(pattern, result_limit)
    statements = translated_statements.queries
    query_type = statements.get('query_type')
    format_type = ""
    final_query = ""
    name_object = 'name'
    hash_object = 'hashes'

    if query_type == 'file':
        if name_object in statements and hash_object in statements and 'folder' in statements:
            file_name = statements.get('name')
            path_value = statements.get('folder')
            hash_value = statements.get('value')
            hash_type = statements.get('hashes')
            format_type = 'file_name_with_hash'
            final_query = RelevanceQueryStringPatternTranslator.query_format.get(format_type).format(name_object=name_object,file_name=file_name,expression_operator=statements.get('expression_operator'),hash_type=hash_type,hash_value=hash_value,file_path=path_value)
        elif hash_object in statements:
            path_value = statements.get('folder')
            hash_type = statements.get('hashes')
            hash_value = statements.get('value')
            format_type = 'file_query'
            final_query = RelevanceQueryStringPatternTranslator.query_format.get(format_type).format(stix_object=hash_type,object_value=hash_value,file_path=path_value)
        elif hash_object not in statements:
            file_name = statements.get('name')
            path_value = statements.get('folder')
            if "*" not in file_name:
                format_type = 'file_query'
                final_query = RelevanceQueryStringPatternTranslator.query_format.get(format_type).format(stix_object=name_object,object_value=file_name,file_path=path_value)
            else:
                format_type = 'all_files_in_directory'
                final_query = RelevanceQueryStringPatternTranslator.query_format.get(format_type).format(file_path=path_value)
    elif query_type == 'process':
        if hash_object not in statements:
            process_name = statements.get('name')
            if "*" not in process_name:
                format_type = 'filter_processes_with_name'
                final_query = RelevanceQueryStringPatternTranslator.query_format.get(format_type).format(process_object=name_object,process_name=process_name)
            else:
                format_type = 'all_processes'
                final_query = RelevanceQueryStringPatternTranslator.query_format.get(format_type)
        else:
            process_name = statements.get('name')
            hash_type = statements.get('hashes')
            hash_value = statements.get('value')
            format_type = 'process_name_with_hash'
            final_query = RelevanceQueryStringPatternTranslator.query_format.get(format_type).format(process_object=name_object,process_name=process_name,expression_operator=statements.get('expression_operator'), hash_type=hash_type,hash_value=hash_value)
    else:
        print('Undefined query type')

    return final_query