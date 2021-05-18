from stix_shifter_utils.utils.error_mapper_base import ErrorMapperBase
from stix_shifter_utils.utils.error_response import ErrorCode
from stix_shifter_utils.stix_translation.src.utils.exceptions import DataMappingException, StixValidationException, \
    UnsupportedDataSourceException, TranslationResultException, UnsupportedDialectException, UnsupportedLanguageException
from stix_shifter_utils.stix_translation.src.patterns.errors import SearchFeatureNotSupportedError
from stix_shifter_utils.utils import logger

error_mapping = {
    NotImplementedError.__name__: [ErrorCode.TRANSLATION_NOTIMPLEMENTED_MODE, 'wrong parameter'],
    DataMappingException.__name__: [ErrorCode.TRANSLATION_MAPPING_ERROR, 'data mapping error'],
    StixValidationException.__name__: [ErrorCode.TRANSLATION_STIX_VALIDATION, 'stix validation error'],
    SearchFeatureNotSupportedError.__name__: [ErrorCode.TRANSLATION_NOTSUPPORTED, 'search feature is not supported'],
    TranslationResultException.__name__: [ErrorCode.TRANSLATION_RESULT, 'result translation error'],
    UnsupportedDataSourceException.__name__: [ErrorCode.TRANSLATION_NOTIMPLEMENTED_MODE, 'unsupported datasource'],
    UnsupportedDialectException.__name__: [ErrorCode.TRANSLATION_UNKNOWN_DIALOG, 'unknown dialect'],
    UnsupportedLanguageException.__name__: [ErrorCode.TRANSLATION_UNKNOWN_LANGUAGE, 'unsupported language']
}


class ErrorMapper():
    logger = logger.set_logger(__name__)
    DEFAULT_ERROR = ErrorCode.TRANSLATION_MODULE_DEFAULT_ERROR

    @staticmethod
    def set_error_code(data_dict, return_obj):
        exception = None
        exception_str = None
        if 'exception' in data_dict:
            exception = data_dict['exception']
            exception_str = str(exception)

        error_code = ErrorMapper.DEFAULT_ERROR
        error_message = 'Error when converting STIX pattern to data source query'
        if exception_str:
            error_message += ': ' + exception_str

        if exception is not None:
            exception_type = type(exception).__name__
            ErrorMapper.logger.error("received exception => {}: {}".format(exception_type, exception))
            ErrorMapper.logger.debug(logger.exception_to_string(exception))
            if exception_type in error_mapping:
                error_code = error_mapping[exception_type][0]
                error_message = error_mapping[exception_type][1]
                exception_message = str(exception)
                if (len(exception_message) > 0):
                    if len(error_message) > 0:
                        error_message += ' : '
                    error_message += exception_message

        ErrorMapperBase.set_error_code(return_obj, error_code, message=error_message)
