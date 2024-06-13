from src.core.exceptions.base import BaseAppError


class InvalidUserDataError(BaseAppError):
    pass


class InvalidEmailError(InvalidUserDataError):
    pass


class InvalidUsernameOrEmailError(InvalidUserDataError):
    pass
