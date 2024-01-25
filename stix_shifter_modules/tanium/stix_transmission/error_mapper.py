from stix_shifter_utils.utils.error_mapper_base import ErrorMapperBase
from stix_shifter_utils.utils.error_response import ErrorCode
from stix_shifter_utils.utils import logger

error_mapping = {
    400: ErrorCode.TRANSMISSION_QUERY_LOGICAL_ERROR.value,
    401: ErrorCode.TRANSMISSION_AUTH_CREDENTIALS.value,
    403: ErrorCode.TRANSMISSION_FORBIDDEN.value,
    404: ErrorCode.TRANSMISSION_QUERY_LOGICAL_ERROR.value,
    405: ErrorCode.TRANSMISSION_QUERY_LOGICAL_ERROR.value,
    407: ErrorCode.TRANSMISSION_AUTH_CREDENTIALS.value,
    411: ErrorCode.TRANSMISSION_QUERY_LOGICAL_ERROR.value,
    429: ErrorCode.TRANSMISSION_TOO_MANY_REQUESTS.value,
    500: ErrorCode.TRANSMISSION_CONNECT.value,
    501: ErrorCode.TRANSMISSION_CONNECT.value,
    502: ErrorCode.TRANSMISSION_CONNECT.value,
    503: ErrorCode.TRANSMISSION_CONNECT.value,
    504: ErrorCode.TRANSMISSION_CONNECT.value,    
}


class ErrorMapper():
    logger = logger.set_logger(__name__)
    DEFAULT_ERROR = ErrorCode.TRANSMISSION_MODULE_DEFAULT_ERROR

    @staticmethod
    def set_error_code(json_data, return_obj, connector=None):
        code = None
        try:
            code = int(json_data.code)
        except Exception:
            pass

        error_code = ErrorMapper.DEFAULT_ERROR

        if code in error_mapping:
            error_code = error_mapping[code]

        if error_code == ErrorMapper.DEFAULT_ERROR:
            ErrorMapper.logger.error("failed to map: " + str(json_data))

        ErrorMapperBase.set_error_code(return_obj, error_code, connector=connector)