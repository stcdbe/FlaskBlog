from src.core.exceptions.base import AbstractAppError


class InvalidPostDataError(AbstractAppError):
    pass


class InvalidPostTitleError(InvalidPostDataError):
    pass
