from stix_shifter_utils.utils.error_mapper_base import ErrorMapperBase
from stix_shifter_utils.utils.error_response import ErrorCode
from stix_shifter_utils.utils import logger

error_mapping = {
    100: ErrorCode.TRANSMISSION_INVALID_PARAMETER,
    120: ErrorCode.TRANSMISSION_CONNECT,
    400: ErrorCode.TRANSMISSION_INVALID_PARAMETER,
    401: ErrorCode.TRANSMISSION_AUTH_CREDENTIALS,
    403: ErrorCode.TRANSMISSION_FORBIDDEN,
    404: ErrorCode.TRANSMISSION_INVALID_PARAMETER,
    429: ErrorCode.TRANSMISSION_CONNECT,
    500: ErrorCode.TRANSMISSION_CONNECT,
    1002: ErrorCode.TRANSMISSION_SEARCH_DOES_NOT_EXISTS,
    1010: ErrorCode.TRANSMISSION_REMOTE_SYSTEM_IS_UNAVAILABLE,
    1015: ErrorCode.TRANSMISSION_AUTH_CREDENTIALS
}


class ErrorMapper:
    """
    Set Error Code
    """
    DEFAULT_ERROR = ErrorCode.TRANSMISSION_MODULE_DEFAULT_ERROR
    logger = logger.set_logger(__name__)

    @staticmethod
    def set_error_code(json_data, return_obj):
        code = None
        try:
            code = int(json_data['code'])
        except Exception:
            pass

        error_code = ErrorMapper.DEFAULT_ERROR

        if code in error_mapping:
            error_code = error_mapping.get(code)

        if error_code == ErrorMapper.DEFAULT_ERROR:
            ErrorMapper.logger.error("failed to map: %s", str(json_data))

        ErrorMapperBase.set_error_code(return_obj, error_code)
