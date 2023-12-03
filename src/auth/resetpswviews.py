from datetime import timedelta
from typing import Any

from flask import redirect, url_for, request, flash, render_template
from flask_jwt_extended import create_access_token, decode_token
from flask_login import current_user
from jwt import ExpiredSignatureError, DecodeError, InvalidTokenError
from werkzeug.security import generate_password_hash

from src import app
from src.auth.authwtforms import PasswordForgotForm, PasswordResetForm
from src.utils import send_email
from src.user.userservice import get_user_by_username_or_email_db, get_user_db, update_user_db
from src.config import RESET_PSW_TOKEN_EXPIRES


@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password() -> Any:
    if current_user.is_authenticated:
        return redirect(url_for('show_main_page'))

    form = PasswordForgotForm()
    if form.validate_on_submit():

        if user := get_user_by_username_or_email_db(username_or_email=form.username_or_email.data):

            token = create_access_token(identity=str(user.id),
                                        expires_delta=timedelta(minutes=RESET_PSW_TOKEN_EXPIRES))
            send_email(subject='(Flask Blog) Reset your password',
                       user=user,
                       url=request.host_url + 'reset_password/' + token,
                       template='resetpswemail.html')
            flash('Further instructions have been sent to your email address.', 'primary')
            return redirect(url_for('signin'))

        flash('Invalid email address.', 'danger')

    return render_template('auth/forgotpassword.html', form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token: str) -> Any:
    if current_user.is_authenticated:
        return redirect(url_for('show_main_page'))

    try:
        user_id = decode_token(encoded_token=token)['sub']
        user = get_user_db(user_id=user_id)

    except ExpiredSignatureError:
        flash('Expired token.', 'danger')
        return redirect(url_for('forgot_password'))

    except (KeyError, DecodeError, InvalidTokenError):
        flash('Invalid token.', 'danger')
        return redirect(url_for('forgot_password'))

    form = PasswordResetForm()
    if form.validate_on_submit():

        hashed_psw = generate_password_hash(password=form.password.data, method='pbkdf2:sha512')
        update_user_db(user=user, upd_data={'password': hashed_psw})
        send_email(subject='(Flask Blog) Your password was reset',
                   user=user,
                   url=request.host_url + 'forgot_password',
                   template='infopswemail.html')
        flash('The new password has been confirmed.', 'primary')
        return redirect(url_for('signin'))

    return render_template('auth/newpassword.html', form=form, token=token)
