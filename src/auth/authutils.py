from typing import Any

from werkzeug.security import generate_password_hash


def prepare_user_data(form_data: dict[str, Any]) -> dict[str, Any]:
    for key in ['submit', 'csrf_token', 'remember', 'repeat_password', 'recaptcha']:
        if key in form_data:
            form_data.pop(key)

    form_data['email'] = form_data['email'].lower()
    form_data['password'] = generate_password_hash(password=form_data['password'])

    return form_data


def prepare_reset_psw_data(password: str) -> dict[str, str]:
    hashed_psw = generate_password_hash(password=password)
    return {'password': hashed_psw}
