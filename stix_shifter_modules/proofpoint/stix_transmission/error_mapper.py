from stix_shifter_utils.utils.error_mapper_base import ErrorMapperBase
from stix_shifter_utils.utils.error_response import ErrorCode
from stix_shifter_utils.utils import logger

error_mapping = {
    2000: ErrorCode.TRANSMISSION_RESPONSE_EMPTY_RESULT,
    4000: ErrorCode.TRANSMISSION_SEARCH_DOES_NOT_EXISTS,
    4010: ErrorCode.TRANSMISSION_AUTH_SSL,
    4020: ErrorCode.TRANSMISSION_REMOTE_SYSTEM_IS_UNAVAILABLE,
    7000: ErrorCode.TRANSMISSION_UNKNOWN
}


class ErrorMapper():

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
            error_code = error_mapping[code]

        if error_code == ErrorMapper.DEFAULT_ERROR:
            ErrorMapper.logger.error("failed to map: " + str(json_data))

        ErrorMapperBase.set_error_code(return_obj, error_code, json_data['message'])
