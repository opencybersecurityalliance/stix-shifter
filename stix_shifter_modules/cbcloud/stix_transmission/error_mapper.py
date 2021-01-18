from stix_shifter_utils.utils.error_mapper_base import ErrorMapperBase
from stix_shifter_utils.utils.error_response import ErrorCode
from stix_shifter_utils.utils import logger


class ErrorMapper():

    DEFAULT_ERROR = ErrorCode.TRANSMISSION_MODULE_DEFAULT_ERROR
    logger = logger.set_logger(__name__)

    @classmethod
    def set_error_code(cls, json_data, return_obj):
        error_code = cls.DEFAULT_ERROR

        try:
            # Carbon Black Cloud stores error messages in 'translation_key'
            error_code = json_data['translation_key']
        except ValueError:
            cls.logger.debug(json_data)

        if error_code == ErrorMapper.DEFAULT_ERROR:
            cls.logger.error(f'failed to map: {str(json_data)}')

        ErrorMapperBase.set_error_code(return_obj, error_code)
