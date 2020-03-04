from stix_shifter_utils.stix_translation.src.patterns.pattern_objects import StartStopQualifier, ObservationExpression, \
    ComparisonExpression, Pattern, CombinedComparisonExpression, CombinedObservationExpression
from stix_shifter_utils.stix_translation.src.utils.exceptions import DataMappingException


class UnmappedAttributeStripper:

    def __init__(self, antlr_object, data_model_mapping):
        self.dmm = data_model_mapping
        self.unmapped_attributes = []
        self.transformed_parsing = self._traverse_parsing_tree(antlr_object)

    def _traverse_combined_expression(self, root):
        expression1 = self._traverse_parsing_tree(root.expr1)
        expression2 = self._traverse_parsing_tree(root.expr2)

        if (not isinstance(root, CombinedObservationExpression) and
            (expression1 == "delete" or expression2 == "delete") and
                root.operator.name == "And"):
            return "delete"

        if (expression1 == "delete" and expression2 == "delete"):
            return "delete"

        if (expression1 == "delete"):
            return expression2

        if (expression2 == "delete"):
            return expression1

        root.expr1 = expression1
        root.expr2 = expression2

        return root

    def _parse_pattern_expression(self, root):
        expression = self._traverse_parsing_tree(root.expression)
        if (expression == "delete"):
            expression = None
        root.expression = expression
        return root

    def _parse_start_stop_qualifier(self, root):
        expression = self._traverse_parsing_tree(root.observation_expression)
        if (expression == "delete"):
            return expression
        root.observation_expression = expression
        return root

    def _parse_observation_expression(self, root):
        if (root.comparison_expression):
            expression = self._traverse_parsing_tree(root.comparison_expression)
            if (expression == "delete"):
                return expression
            root.comparison_expression = expression
        return root

    def _parse_comparison_expression(self, root):
        stix_object, stix_field = root.object_path.split(':')
        mapped_fields_array = self.dmm.map_field(stix_object, stix_field)
        if not mapped_fields_array:
            self.unmapped_attributes.append(root.object_path)
            return "delete"
        else:
            return root

    def _traverse_parsing_tree(self, root):
        if root:
            if isinstance(root, Pattern):
                root = self._parse_pattern_expression(root)
            if isinstance(root, StartStopQualifier):
                root = self._parse_start_stop_qualifier(root)
            if isinstance(root, CombinedObservationExpression):
                return self._traverse_combined_expression(root)
            if isinstance(root, ObservationExpression):
                root = self._parse_observation_expression(root)
            if isinstance(root, CombinedComparisonExpression):
                return self._traverse_combined_expression(root)
            if isinstance(root, ComparisonExpression):
                root = self._parse_comparison_expression(root)
            return root


def strip_unmapped_attributes(antlr_parsing, data_model_mapping=None):
    if not data_model_mapping:
        return antlr_parsing
    attribute_stripper = UnmappedAttributeStripper(antlr_parsing, data_model_mapping)
    modified_antlr_parsing = attribute_stripper.transformed_parsing
    if not modified_antlr_parsing.expression:
        modified_antlr_parsing = None
    return {"parsing": modified_antlr_parsing, "unmapped_stix": attribute_stripper.unmapped_attributes}