from stix_shifter_utils.utils.error_mapper_base import ErrorMapperBase
from stix_shifter_utils.utils.error_response import ErrorCode
from stix_shifter_utils.utils import logger

ERROR_MAPPING = {
    "InvalidRequestException": ErrorCode.TRANSMISSION_INVALID_PARAMETER,
    "ParamValidationError": ErrorCode.TRANSMISSION_INVALID_PARAMETER,
    "InternalServerException": ErrorCode.TRANSMISSION_CONNECT,
    "TooManyRequestsException": ErrorCode.TRANSMISSION_QUERY_LOGICAL_ERROR,
    "ClientError": ErrorCode.TRANSMISSION_AUTH_CREDENTIALS,
    "AccessDeniedException": ErrorCode.TRANSMISSION_AUTH_CREDENTIALS,
    "InvalidParameterException": ErrorCode.TRANSMISSION_INVALID_PARAMETER
    }


class ErrorMapper:
    """"ErrorMapper class"""
    logger = logger.set_logger(__name__)
    DEFAULT_ERROR = ErrorCode.TRANSMISSION_MODULE_DEFAULT_ERROR

    @staticmethod
    def set_error_code(json_data, return_obj):
        """aws transmit specified error
         :param json_data: dict, error response of api_call
         :param return_obj: dict, returns error and error code"""
        error_type = ''
        try:
            error_type = json_data['__type']
        except KeyError:
            pass

        error_code = ErrorMapper.DEFAULT_ERROR

        if error_type in ERROR_MAPPING:
            error_code = ERROR_MAPPING[error_type]

        if error_code == ErrorMapper.DEFAULT_ERROR:
            ErrorMapper.logger.debug("failed to map: " + str(json_data))

        ErrorMapperBase.set_error_code(return_obj, error_code)
