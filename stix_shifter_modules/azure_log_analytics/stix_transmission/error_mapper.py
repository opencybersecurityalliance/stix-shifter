from stix_shifter_utils.utils.error_mapper_base import ErrorMapperBase
from stix_shifter_utils.utils.error_response import ErrorCode
from stix_shifter_utils.utils import logger

error_mapping = {
    400: ErrorCode.TRANSMISSION_QUERY_PARSING_ERROR,
    401: ErrorCode.TRANSMISSION_AUTH_CREDENTIALS,
    404: ErrorCode.TRANSMISSION_INVALID_PARAMETER,
    408: ErrorCode.TRANSMISSION_CONNECT,
    500: ErrorCode.TRANSMISSION_REMOTE_SYSTEM_IS_UNAVAILABLE
}


class ErrorMapper:
    """"ErrorMapper class"""
    logger = logger.set_logger(__name__)
    DEFAULT_ERROR = ErrorCode.TRANSMISSION_MODULE_DEFAULT_ERROR

    @staticmethod
    def set_error_code(json_data, return_obj, connector=None):
        """azure log analytics transmit specified error
        :param json_data: dict, error response of api_call
        :param return_obj: dict, returns error and error code"""
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

        ErrorMapperBase.set_error_code(return_obj, error_code, connector=connector)
