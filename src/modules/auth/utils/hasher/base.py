from abc import ABC, abstractmethod


class AbstractHasher(ABC):
    @staticmethod
    @abstractmethod
    def get_psw_hash(psw: str) -> str: ...

    @staticmethod
    @abstractmethod
    def verify_psw(psw_to_check: str, hashed_psw: str) -> bool: ...
