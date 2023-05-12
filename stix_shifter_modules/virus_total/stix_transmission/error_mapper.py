from stix_shifter_utils.utils.error_mapper_base import ErrorMapperBase
from stix_shifter_utils.utils.error_response import ErrorCode
from stix_shifter_utils.utils import logger

error_mapping = {
    # These are only examples. Change the keys to reflect the error codes that come back from the data source API.
    # search does not exist
    1002: ErrorCode.TRANSMISSION_SEARCH_DOES_NOT_EXISTS,
    # The search cannot be created. The requested search ID that was provided in the query expression is already in use.
    # Please use a unique search ID (or allow one to be generated).
    1004: ErrorCode.TRANSMISSION_MODULE_DEFAULT_ERROR.value,
    # A request parameter is not valid
    1005: ErrorCode.TRANSMISSION_INVALID_PARAMETER,
    # The server might be temporarily unavailable or offline. Please try again later.
    1010: ErrorCode.TRANSMISSION_REMOTE_SYSTEM_IS_UNAVAILABLE,
    # An error occurred during the attempt
    1020: ErrorCode.TRANSMISSION_MODULE_DEFAULT_ERROR.value,
    #error in query
    2000: ErrorCode.TRANSMISSION_QUERY_PARSING_ERROR
}


class ErrorMapper():
    logger = logger.set_logger(__name__)
    DEFAULT_ERROR = ErrorCode.TRANSMISSION_MODULE_DEFAULT_ERROR

    @staticmethod
    def set_error_code(json_data, return_obj):
        code = None
        try:
            code = int(json_data['code'])
        except Exception:
            pass

        error_code = ErrorMapper.DEFAULT_ERROR

        if code in error_mapping:
            error_code = error_mapping[code]

        if error_code == ErrorMapper.DEFAULT_ERROR:
            ErrorMapper.logger.error("failed to map: " + str(json_data))

        ErrorMapperBase.set_error_code(return_obj, error_code)
