from abc import ABC, abstractmethod


class AbstractHasher(ABC):
    @abstractmethod
    def get_psw_hash(self, psw: str) -> str: ...

    @abstractmethod
    def verify_psw(self, psw_to_check: str, hashed_psw: str) -> bool: ...
