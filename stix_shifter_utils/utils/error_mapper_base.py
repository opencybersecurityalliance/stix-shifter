from enum import Enum

class ErrorMapperBase():
    @staticmethod
    def set_error_code(return_obj, code, message=None):
        if isinstance(code, Enum):
            return_obj['code'] = code.value
        else:
            return_obj['code'] = code
        if message is not None:
            return_obj['error'] = message