from stix_shifter.stix_translation.src.patterns.pattern_objects import StartStopQualifier, ObservationExpression, \
    ComparisonExpression, Pattern, CombinedComparisonExpression, CombinedObservationExpression
from stix_shifter.stix_translation.src.utils.exceptions import DataMappingException


class UnmappedAttributeStripper:

    def __init__(self, antlr_object, data_model_mapping):
        self.dmm = data_model_mapping
        self.unmapped_attributes = ''
        self.transformed_parsing = self._traverse(antlr_object)

    def _traverse_combined_expression(self, root):
        res1 = self._traverse(root.expr1)
        res2 = self._traverse(root.expr2)

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

    def _traverse(self, root):
        if root:
            if isinstance(root, Pattern):
                res = self._traverse(root.expression)
                if (res == "delete"):
                    res = None
                root.expression = res

            if isinstance(root, StartStopQualifier):
                res = self._traverse(root.observation_expression)
                if (res == "delete"):
                    return res
                root.observation_expression = res
            if isinstance(root, CombinedObservationExpression):
                return self._traverse_combined_expression(root)

            if isinstance(root, ObservationExpression):
                if (root.comparison_expression):
                    res = self._traverse(root.comparison_expression)
                    if (res == "delete"):
                        return res
                    root.comparison_expression = res

            if isinstance(root, CombinedComparisonExpression):
                return self._traverse_combined_expression(root)

            if isinstance(root, ComparisonExpression):
                stix_object, stix_field = root.object_path.split(':')
                mapped_fields_array = self.dmm.map_field(stix_object, stix_field)
                if not mapped_fields_array:
                    self.unmapped_attributes += " {}".format(root.object_path)
                    return "delete"

            return root


def strip_unmapped_attributes(antlr_parsing, data_model_mapping):
    attribute_stripper = UnmappedAttributeStripper(antlr_parsing, data_model_mapping)
    modified_antlr_parsing = attribute_stripper.transformed_parsing
    if not modified_antlr_parsing.expression:
        raise DataMappingException("Unable to map the following STIX attributes to data source fields:{}".format(attribute_stripper.unmapped_attributes))
    return modified_antlr_parsing
