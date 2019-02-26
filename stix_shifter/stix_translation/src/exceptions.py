class DataMappingException(Exception):
    pass


class StixValidationException(Exception):
    pass


class TranslationResultException(Exception):
    def __str__(self):
        return "Error when converting results to STIX"


class UnsupportedDataSourceException(Exception):
    pass
