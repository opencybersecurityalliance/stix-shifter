__all__ = ["AiogoogleError", "ValidationError", "HTTPError", "AuthError"]


class AiogoogleError(Exception):
    pass


class ValidationError(AiogoogleError):
    """
    Raised when the validate flag is set true and a validation error occurs
    """

    pass


class HTTPError(AiogoogleError):
    def __init__(self, msg, req=None, res=None):
        self.req = req
        self.res = res
        super().__init__(msg)


class AuthError(HTTPError):
    pass
