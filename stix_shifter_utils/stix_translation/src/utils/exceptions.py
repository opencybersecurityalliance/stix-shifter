class DataMappingException(Exception):
    pass


class StixValidationException(Exception):
    pass


class TranslationResultException(Exception):
    pass


class LoadJsonResultsException(Exception):
    def __str__(self):
        return "Error when loading the JSON results from the data source"


class UnsupportedDataSourceException(Exception):
    pass
