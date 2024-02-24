class InvalidUserDataError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)

    def __str__(self) -> str:
        return self.message


class InvalidEmailError(InvalidUserDataError):
    pass


class InvalidUsernameOrEmailError(InvalidUserDataError):
    pass


class InvalidTokenError(InvalidUserDataError):
    pass
