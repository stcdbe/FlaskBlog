from enum import Enum


class UserStatus(str, Enum):
    Default = 'Default'
    Author = 'Author'
    Admin = 'Admin'
