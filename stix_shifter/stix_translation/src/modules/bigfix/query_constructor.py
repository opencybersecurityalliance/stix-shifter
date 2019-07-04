from stix_shifter.stix_translation.src.patterns.pattern_objects import ObservationExpression, ComparisonExpression, \
    ComparisonExpressionOperators, ComparisonComparators, Pattern, \
    CombinedComparisonExpression, CombinedObservationExpression, ObservationOperators
from stix_shifter.stix_translation.src.patterns.errors import SearchFeatureNotSupportedError
import logging

logger = logging.getLogger(__name__)


class RelevanceQueryStringPatternTranslator:
    comparator_lookup = {
        ComparisonExpressionOperators.And: "AND",
        ComparisonExpressionOperators.Or: "OR",
        ComparisonComparators.Equal: "=",
        ComparisonComparators.NotEqual: "!=",
        ComparisonComparators.Like: "contains",
        ObservationOperators.Or: 'OR',
        # Treat AND's as OR's -- Unsure how two ObsExps wouldn't cancel each other out.
        ObservationOperators.And: 'OR'
    }

    query_format = {
        "all_files_in_directory": "(\"file\", name of it | \"n/a\", \"sha256\", sha256 of it | \"n/a\", \"sha1\", sha1 of it | \"n/a\", \"md5\", md5 of it | \"n/a\", pathname of it | \"n/a\", (modification time of it - \"01 Jan 1970 00:00:00 +0000\" as time)/second ) of files of folder (\"{file_path}\")",
        "file_query": "(\"file\", name of it | \"n/a\", \"sha256\", sha256 of it | \"n/a\", \"sha1\", sha1 of it | \"n/a\", \"md5\", md5 of it | \"n/a\", pathname of it | \"n/a\", (modification time of it - \"01 Jan 1970 00:00:00 +0000\" as time)/second ) of files whose ({stix_object} of it as lowercase {object_value} as lowercase) of folder (\"{file_path}\")",
        "file_name_with_hash": "(\"file\", name of it | \"n/a\", \"sha256\", sha256 of it | \"n/a\", \"sha1\", sha1 of it | \"n/a\", \"md5\", md5 of it | \"n/a\", pathname of it | \"n/a\", (modification time of it - \"01 Jan 1970 00:00:00 +0000\" as time)/second ) of files whose ({name_object} of it as lowercase {file_name} as lowercase {expression_operator} {hash_type} of it as lowercase {hash_value} as lowercase) of folder (\"{file_path}\")",
        "all_processes": "( \"process\", name of it | \"n/a\", process id of it as string | \"n/a\", \"sha256\", sha256 of image file of it | \"n/a\", \"sha1\", sha1 of image file of it | \"n/a\", \"md5\", md5 of image file of it | \"n/a\", pathname of image file of it | \"n/a\", (start time of it - \"01 Jan 1970 00:00:00 +0000\" as time)/second ) of processes",
        "filter_processes_with_name": "( \"process\", name of it | \"n/a\", process id of it as string | \"n/a\", \"sha256\", sha256 of image file of it | \"n/a\", \"sha1\", sha1 of image file of it | \"n/a\", \"md5\", md5 of image file of it | \"n/a\", pathname of image file of it | \"n/a\", (start time of it - \"01 Jan 1970 00:00:00 +0000\" as time)/second ) of processes whose ({process_object} of it as lowercase {process_name} as lowercase )",
        "process_hash_query": "( \"process\", name of it | \"n/a\", process id of it as string | \"n/a\", \"sha256\", sha256 of image file of it | \"n/a\", \"sha1\", sha1 of image file of it | \"n/a\", \"md5\", md5 of image file of it | \"n/a\", pathname of image file of it | \"n/a\", (start time of it - \"01 Jan 1970 00:00:00 +0000\" as time)/second ) of processes whose ({hash_type} of image file of it as lowercase {hash_value} as lowercase )",
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
                self.query_string.update({reference_property: value})
            else:
                if stix_key != "":
                    reference_property = stix_key
                    self.query_string.update({stix_property: stix_key})
                    self.query_string.update({'value': final_value})
                else:
                    self.query_string.update({stix_object: final_value})

            self.query_string.update({'comparator': comparator})

            return self.query_string
        elif isinstance(expression, CombinedComparisonExpression):
            self._parse_expression(expression.expr1)
            expression_operator = self.comparator_lookup[expression.operator]
            self._parse_expression(expression.expr2)

            self.query_string.update({'expression_operator': expression_operator})

            if qualifier is not None:
                logger.info("Qualifier is not supported in BigFix relevance query.")

            return self.query_string
        elif isinstance(expression, ObservationExpression):
            return self._parse_expression(expression.comparison_expression, qualifier)
        elif isinstance(expression, Pattern):
            return self._parse_expression(expression.expression)
        else:
            raise RuntimeError("Unknown Recursion Case for expression={}, type(expression)={}".format(
                expression, type(expression)))

    def parse_expression(self, pattern: Pattern):
        return self._parse_expression(pattern)


def translate_pattern(pattern: Pattern, options):
    result_limit = options['result_limit']
    # timerange = options['timerange']
    query_dictionary = {}
    translated_dictionary = RelevanceQueryStringPatternTranslator(pattern, result_limit)
    query_dictionary = translated_dictionary.queries

    format_type = ""
    final_query = ""
    name_object = 'name'
    process_object = 'process'
    file_object = 'file'
    hash_object = 'hashes'
    value_object = 'value'
    directory_alias = 'folder'

    if hash_object in query_dictionary:
        hash_type = query_dictionary.get(hash_object)
        if '-' in hash_type:
            hash_type = hash_type.replace('-', '').lower()

    if file_object in query_dictionary:
        if file_object in query_dictionary and hash_object in query_dictionary and directory_alias in query_dictionary:
            file_name = query_dictionary.get(file_object)
            path_value = query_dictionary.get(directory_alias)
            hash_value = query_dictionary.get(value_object)
            format_type = 'file_name_with_hash'
            final_query = RelevanceQueryStringPatternTranslator.query_format.get(format_type).format(name_object=name_object, file_name=file_name,
                                                                                                     expression_operator=query_dictionary.get('expression_operator'), hash_type=hash_type, hash_value=hash_value, file_path=path_value)
        elif hash_object in query_dictionary and directory_alias in query_dictionary:
            path_value = query_dictionary.get(directory_alias)
            hash_value = query_dictionary.get(value_object)
            format_type = 'file_query'
            final_query = RelevanceQueryStringPatternTranslator.query_format.get(format_type).format(stix_object=hash_type, object_value=hash_value, file_path=path_value)
        elif hash_object not in query_dictionary:
            file_name = query_dictionary.get(file_object)
            path_value = query_dictionary.get(directory_alias)
            if "*" not in file_name:
                format_type = 'file_query'
                final_query = RelevanceQueryStringPatternTranslator.query_format.get(format_type).format(stix_object=name_object, object_value=file_name, file_path=path_value)
            else:
                format_type = 'all_files_in_directory'
                final_query = RelevanceQueryStringPatternTranslator.query_format.get(format_type).format(file_path=path_value)
    elif process_object in query_dictionary:
        process_name = query_dictionary.get(process_object)
        if hash_object not in query_dictionary:
            if "*" not in process_name:
                format_type = 'filter_processes_with_name'
                final_query = RelevanceQueryStringPatternTranslator.query_format.get(format_type).format(process_object=name_object, process_name=process_name)
            else:
                format_type = 'all_processes'
                final_query = RelevanceQueryStringPatternTranslator.query_format.get(format_type)
        else:
            hash_value = query_dictionary.get(value_object)
            format_type = 'process_name_with_hash'
            final_query = RelevanceQueryStringPatternTranslator.query_format.get(format_type).format(process_object=name_object, process_name=process_name,
                                                                                                     expression_operator=query_dictionary.get('expression_operator'), hash_type=hash_type, hash_value=hash_value)
    elif hash_object in query_dictionary and directory_alias in query_dictionary:
        path_value = query_dictionary.get(directory_alias)
        hash_value = query_dictionary.get(value_object)
        format_type = 'file_query'
        final_query = RelevanceQueryStringPatternTranslator.query_format.get(format_type).format(stix_object=hash_type, object_value=hash_value, file_path=path_value)
    elif hash_object in query_dictionary:
        hash_value = query_dictionary.get(value_object)
        format_type = 'process_hash_query'
        final_query = RelevanceQueryStringPatternTranslator.query_format.get(format_type).format(hash_type=hash_type, hash_value=hash_value)
    else:
        logger.info('Unable to translate the Stix pattern into Relevance query')

        return 'Unable to translate the Stix pattern into Relevance query'

    besapi_query = '<BESAPI xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xsi:noNamespaceSchemaLocation=\"BESAPI.xsd\"><ClientQuery><ApplicabilityRelevance>true</ApplicabilityRelevance><QueryText>' + \
        final_query + '</QueryText><Target><CustomRelevance>true</CustomRelevance></Target></ClientQuery></BESAPI>'

    # Clearing out the query dictionary as we no longer need.
    RelevanceQueryStringPatternTranslator.query_string.clear()

    return besapi_query
