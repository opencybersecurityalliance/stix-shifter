from ..utils.error_mapper_base import ErrorMapperBase
from ..utils.error_response import ErrorCode
from .src.exceptions import DataMappingException, StixValidationException, UnsupportedDataSourceException, TranslationResultException
from .src.patterns.errors import SearchFeatureNotSupportedError

error_mapping = {
    NotImplementedError.__name__: ErrorCode.TRANSLATION_NOTIMPLEMENTED_MODE,
    DataMappingException.__name__: ErrorCode.TRANSLATION_MAPPING_ERROR,
    StixValidationException.__name__: ErrorCode.TRANSLATION_STIX_VALIDATION,
    SearchFeatureNotSupportedError.__name__: ErrorCode.TRANSLATION_NOTSUPPORTED,
    TranslationResultException.__name__: ErrorCode.TRANSLATION_RESULT,
    UnsupportedDataSourceException.__name__: ErrorCode.TRANSLATION_NOTIMPLEMENTED_MODE
}


class ErrorMapper():

    DEFAULT_ERROR = ErrorCode.TRANSLATION_MODULE_DEFAULT_ERROR

    @staticmethod
    def set_error_code(data_dict, return_obj):
        exception = None
        if 'exception' in data_dict:
            exception = data_dict['exception']

        error_code = ErrorMapper.DEFAULT_ERROR
        error_message = 'Error when converting STIX pattern to data source query'

        if exception is not None:
            exception_type = type(exception).__name__
            print("received exception => {}: {}".format(exception_type, exception))
            if exception_type in error_mapping:
                error_code = error_mapping[exception_type]
                error_message = str(exception)

        ErrorMapperBase.set_error_code(return_obj, error_code, message=error_message)
