""""Azure Sentinal connector specified error handling"""
from stix_shifter_utils.utils.error_mapper_base import ErrorMapperBase
from stix_shifter_utils.utils.error_response import ErrorCode
from stix_shifter_utils.utils import logger

ERROR_MAPPING = {
    "json_parse_exception": ErrorCode.TRANSMISSION_QUERY_PARSING_ERROR,
    "HTTPSConnectionError": ErrorCode.TRANSMISSION_CONNECT,
    "invalid_instance": ErrorCode.TRANSMISSION_INVALID_PARAMETER,
    "invalid_request": ErrorCode.TRANSMISSION_AUTH_CREDENTIALS,
    "invalid_client": ErrorCode.TRANSMISSION_AUTH_CREDENTIALS,
    "unauthorized_client": ErrorCode.TRANSMISSION_AUTH_CREDENTIALS,
    # Azure specific exception
    "BadRequest": ErrorCode.TRANSMISSION_INVALID_PARAMETER,
    "InvalidAuthenticationToken": ErrorCode.TRANSMISSION_AUTH_CREDENTIALS,
    "accessDenied": ErrorCode.TRANSMISSION_AUTH_CREDENTIALS,
    "activityLimitReached": ErrorCode.TRANSMISSION_SEARCH_DOES_NOT_EXISTS,
    "generalException": ErrorCode.TRANSMISSION_QUERY_PARSING_ERROR,
    "invalidRange": ErrorCode.TRANSMISSION_RESPONSE_EMPTY_RESULT,
    "invalidRequest": ErrorCode.TRANSMISSION_INVALID_PARAMETER,
    "itemNotFound": ErrorCode.TRANSMISSION_RESPONSE_EMPTY_RESULT,
    "malwareDetected": ErrorCode.TRANSMISSION_INVALID_PARAMETER,
    "nameAlreadyExists": ErrorCode.TRANSMISSION_QUERY_LOGICAL_ERROR,
    "notAllowed": ErrorCode.TRANSMISSION_CONNECT,
    "notSupported": ErrorCode.TRANSMISSION_CONNECT,
    "resourceModified": ErrorCode.TRANSMISSION_INVALID_PARAMETER,
    "resyncRequired": ErrorCode.TRANSMISSION_INVALID_PARAMETER,
    "serviceNotAvailable": ErrorCode.TRANSMISSION_CONNECT,
    "quotaLimitReached": ErrorCode.TRANSMISSION_SEARCH_DOES_NOT_EXISTS,
    "unauthenticated": ErrorCode.TRANSMISSION_AUTH_CREDENTIALS,
    "ResourceNotFound": ErrorCode.TRANSMISSION_INVALID_PARAMETER,
    }


class ErrorMapper:
    """"ErrorMapper class"""
    logger = logger.set_logger(__name__)
    DEFAULT_ERROR = ErrorCode.TRANSMISSION_MODULE_DEFAULT_ERROR

    @staticmethod
    def set_error_code(json_data, return_obj):
        """ms_atp transmit specified error
         :param json_data: dict, error response of api_call
         :param return_obj: dict, returns error and error code"""
        error_type = ''
        
        if isinstance(json_data, tuple):
            error_type = 'HTTPSConnectionError'
        else:
            try:
                error_type = json_data['error']['code']
            except Exception:
                error_type = json_data['error']

        error_code = ErrorMapper.DEFAULT_ERROR

        if error_type in ERROR_MAPPING:
            error_code = ERROR_MAPPING[error_type]

        if error_code == ErrorMapper.DEFAULT_ERROR:
            ErrorMapper.logger.debug("failed to map: " + str(json_data))

        ErrorMapperBase.set_error_code(return_obj, error_code)
