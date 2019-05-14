import logging

from ...patterns.parser import generate_query
from ..base.base_query_translator import BaseQueryTranslator
from . import data_mapping
from . import query_constructor
from ...patterns.pattern_objects import StartStopQualifier, ObservationExpression, \
    ComparisonExpression, ComparisonExpressionOperators, ComparisonComparators, Pattern, \
    CombinedComparisonExpression, CombinedObservationExpression, ObservationOperators

logger = logging.getLogger(__name__)


class StixToQuery(BaseQueryTranslator):

    def traverseCombinedExpression(self, root):
        res1 = self.traverse(root.expr1)
        res2 = self.traverse(root.expr2)

        if (res1 == "delete" or res2 == "delete"):
            if (root.operator.name == "And"):
                return "delete"

        if (res1 == "delete" and res2 == "delete"):
            return "delete"

        if (res1 == "delete"):
            return res2

        if (res2 == "delete"):
            return res1

        root.expr1 = res1
        root.expr2 = res2

        return root

    def traverse(self, root):

        if root:
            if isinstance(root, Pattern):
                res = self.traverse(root.expression)
                if (res == "delete"):
                    res = None
                root.expression = res

            if isinstance(root, StartStopQualifier):
                res = self.traverse(root.observation_expression)
                if (res == "delete"):
                    return res
                root.observation_expression = res
            if isinstance(root, CombinedObservationExpression):
                return self.traverseCombinedExpression(root)

            if isinstance(root, ObservationExpression):
                if (root.comparison_expression):
                    res = self.traverse(root.comparison_expression)
                    if (res == "delete"):
                        return res
                    root.comparison_expression = res

            if isinstance(root, CombinedComparisonExpression):
                return self.traverseCombinedExpression(root)

            if isinstance(root, ComparisonExpression):
                if (root.object_path == "network-traffic:dst_port"):
                    return "delete"

            return root

    def transform_query(self, data, options, mapping=None):
        """
        Transforms STIX query into data source query format. Based on a mapping file
        :param data: STIX query string to transform into data source query format
        :type data: str
        :param mapping: The mapping file path to use as instructions on how to transform the given STIX query into data source query format.
        :type mapping: str (filepath)
        :return: data source query string
        :rtype: str
        """

        logger.info("Converting STIX2 Pattern to data source query")

        query_object = generate_query(data)
        query_object = self.traverse(query_object)

        data_model_mapper = data_mapping.DataMapper(options)

        query_string = query_constructor.translate_pattern(
            query_object, data_model_mapper, options)
        return query_string
