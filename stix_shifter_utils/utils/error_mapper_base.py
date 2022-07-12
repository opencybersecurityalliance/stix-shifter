from enum import Enum

class ErrorMapperBase():
    @staticmethod
    def set_error_code(return_obj, code, message=None, connector=None):
        if isinstance(code, Enum):
            return_obj['code'] = code.value
        else:
            return_obj['code'] = code
        if message is not None:
            if connector:
                return_obj['error'] = '{} connector error => {}'.format(connector, str(message))
            elif return_obj.get('connector'):
                return_obj['error'] = '{} connector error => {}'.format(return_obj['connector'], str(message))
            else:
                return_obj['error'] = message