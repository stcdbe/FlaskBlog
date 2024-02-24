from enum import StrEnum, auto


class UserStatus(StrEnum):
    default = auto()
    author = auto()
    admin = auto()
