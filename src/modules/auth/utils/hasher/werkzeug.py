from werkzeug.security import check_password_hash, generate_password_hash

from src.modules.auth.utils.hasher.base import AbstractHasher


class WerkzeugHasher(AbstractHasher):
    @staticmethod
    def get_psw_hash(psw: str) -> str:
        return generate_password_hash(password=psw)

    @staticmethod
    def verify_psw(psw_to_check: str, hashed_psw: str) -> bool:
        return check_password_hash(pwhash=hashed_psw, password=psw_to_check)
