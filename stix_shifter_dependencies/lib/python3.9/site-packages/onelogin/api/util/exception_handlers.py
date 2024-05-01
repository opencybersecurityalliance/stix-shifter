#!/usr/bin/python


def exception_handler(func):
    def decorator(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except Exception as e:
            self.error = 500
            self.error_description = e.args[0]

    return decorator


def exception_handler_return_false(func):
    def decorator(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except Exception as e:
            self.error = 500
            self.error_description = e.args[0]
        return False

    return decorator
