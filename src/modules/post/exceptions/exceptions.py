from src.core.exceptions.base import BaseAppError


class InvalidPostDataError(BaseAppError):
    pass


class InvalidPostTitleError(InvalidPostDataError):
    pass
