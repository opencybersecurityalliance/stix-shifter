from .....utils.error_mapper_base import ErrorMapperBase
from .....utils.error_response import ErrorCode

error_mapping = {
        "json_parse_exception"              : ErrorCode.TRANSMISSION_QUERY_PARSING_ERROR,
        "query_phase_execution_exception"   : ErrorCode.TRANSMISSION_QUERY_PARSING_ERROR,
        "illegal_argument_exception"        : ErrorCode.TRANSMISSION_INVALID_PARAMETER,
        "search_phase_execution_exception"  : ErrorCode.TRANSMISSION_INVALID_PARAMETER
    }

class ErrorMapper():

    DEFAULT_ERROR = ErrorCode.TRANSMISSION_MODULE_DEFAULT_ERROR

    @staticmethod
    def set_error_code(json_data, return_obj):
        code = None
        try:
            error_type = json_data['error']['type']
        except Exception:
            pass

        error_code = ErrorMapper.DEFAULT_ERROR

        if error_type in error_mapping:
            error_code = error_mapping[error_type]

        if error_code == ErrorMapper.DEFAULT_ERROR:
            print("failed to map: "+ str(json_data))

        ErrorMapperBase.set_error_code(return_obj, error_code)
