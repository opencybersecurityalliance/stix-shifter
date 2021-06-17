from stix_shifter_utils.utils import logger
from stix_shifter_utils.utils.error_mapper_base import ErrorMapperBase
from stix_shifter_utils.utils.error_response import ErrorCode

error_mapping = {
    400: ErrorCode.TRANSLATION_NOTSUPPORTED,
    401: ErrorCode.TRANSMISSION_AUTH_CREDENTIALS,
    500: ErrorCode.TRANSMISSION_REMOTE_SYSTEM_IS_UNAVAILABLE,
    599: ErrorCode.TRANSMISSION_REMOTE_SYSTEM_IS_UNAVAILABLE,
}


class ErrorMapper:
    logger = logger.set_logger(__name__)
    DEFAULT_ERROR = ErrorCode.TRANSMISSION_MODULE_DEFAULT_ERROR

    @staticmethod
    def set_error_code(json_data, return_obj):
        code = None
        try:
            code = int(json_data['code'])
        except Exception:
            pass

        error_code = error_mapping.get(code, ErrorMapper.DEFAULT_ERROR)

        if error_code == ErrorMapper.DEFAULT_ERROR:
            ErrorMapper.logger.error("failed to map: %s", json_data)

        ErrorMapperBase.set_error_code(return_obj, error_code)
