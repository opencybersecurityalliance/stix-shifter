from stix_shifter_utils.stix_translation.src.utils.transformers import ValueTransformer

class VerifyStaticTransformer(ValueTransformer):
    """A value transformer that always returns the string 'IBM Security Verify IAM'"""

    @staticmethod
    def transform(value):
        return "IBM Security Verify IAM"