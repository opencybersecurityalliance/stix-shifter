from stix_shifter_utils.utils.error_mapper_base import ErrorMapperBase
from stix_shifter_utils.utils.error_response import ErrorCode
from stix_shifter_utils.utils import logger

error_mapping = {
    # Authentication Failure
    403: ErrorCode.TRANSMISSION_FORBIDDEN,
    # A request parameter is not valid
    400: ErrorCode.TRANSMISSION_INVALID_PARAMETER,
    1004: ErrorCode.TRANSMISSION_AUTH_SSL
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
