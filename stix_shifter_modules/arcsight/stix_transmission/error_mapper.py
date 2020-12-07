from stix_shifter_utils.utils.error_mapper_base import ErrorMapperBase
from stix_shifter_utils.utils.error_response import ErrorCode
from stix_shifter_utils.utils import logger

ERROR_MAPPING = {
    1002: ErrorCode.TRANSMISSION_AUTH_CREDENTIALS,
    1003: ErrorCode.TRANSMISSION_AUTH_CREDENTIALS,
    1004: ErrorCode.TRANSMISSION_AUTH_SSL,
    1005: ErrorCode.TRANSMISSION_AUTH_SSL,
    1009: ErrorCode.TRANSMISSION_CONNECT,
    1010: ErrorCode.TRANSMISSION_INVALID_PARAMETER,
    1100: ErrorCode.TRANSMISSION_INVALID_PARAMETER,
    1111: ErrorCode.TRANSMISSION_QUERY_PARSING_ERROR,
    'ConnectionError': ErrorCode.TRANSMISSION_CONNECT,
    'SyntaxError': ErrorCode.TRANSMISSION_INVALID_PARAMETER,
    'unknown': ErrorCode.TRANSMISSION_UNKNOWN
}


class ErrorMapper:
    """"ErrorMapper class"""
    logger = logger.set_logger(__name__)
    DEFAULT_ERROR = ErrorCode.TRANSMISSION_MODULE_DEFAULT_ERROR

    @staticmethod
    def set_error_code(json_data, return_obj):
        """arcsight transmit specified error
        :param json_data: dict, error response of api_call
        :param return_obj: dict, returns error and error code"""
        try:
            error_type = json_data['code']

        except Exception:
            error_type = json_data.__class__.__name__

        # logger down string error mapping
        if 'currently unavailable' in str(json_data):
            error_type = 'ConnectionError'

        error_code = ErrorMapper.DEFAULT_ERROR

        if error_type in ERROR_MAPPING:
            error_code = ERROR_MAPPING[error_type]

        if error_code == ErrorMapper.DEFAULT_ERROR:
            ErrorMapper.logger.debug("failed to map: " + str(json_data))

        ErrorMapperBase.set_error_code(return_obj, error_code)
