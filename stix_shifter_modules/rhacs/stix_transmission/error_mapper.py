"""this module is used to map the user defined error"""
from stix_shifter_utils.utils.error_mapper_base import ErrorMapperBase
from stix_shifter_utils.utils.error_response import ErrorCode
from stix_shifter_utils.utils import logger

error_mapping = {
    "AuthenticationError": ErrorCode.TRANSMISSION_AUTH_CREDENTIALS,
    "ConnectionError": ErrorCode.TRANSMISSION_REMOTE_SYSTEM_IS_UNAVAILABLE,
    "RetryError": ErrorCode.TRANSMISSION_INVALID_PARAMETER
}


class ErrorMapper():
    """Error Mapper Class"""
    logger = logger.set_logger(__name__)
    DEFAULT_ERROR = ErrorCode.TRANSMISSION_MODULE_DEFAULT_ERROR

    @staticmethod
    def set_error_code(json_data, return_obj):
        """Set Error Code"""
        err_type = None
        try:
            err_type = json_data['type']
        except KeyError:
            pass

        error_type = ErrorMapper.DEFAULT_ERROR

        if err_type in error_mapping:
            error_type = error_mapping.get(err_type)

        if error_type == ErrorMapper.DEFAULT_ERROR:
            ErrorMapper.logger.error("failed to map: %s", str(json_data))

        ErrorMapperBase.set_error_code(return_obj, error_type)
