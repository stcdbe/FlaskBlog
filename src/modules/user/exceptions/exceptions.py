from src.core.exceptions.base import AbstractAppError


class InvalidUserDataError(AbstractAppError):
    pass


class InvalidEmailError(InvalidUserDataError):
    pass


class InvalidUsernameOrEmailError(InvalidUserDataError):
    pass


class InvalidJWTError(InvalidUserDataError):
    pass
