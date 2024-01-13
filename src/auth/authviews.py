from datetime import timedelta
from typing import Any
from uuid import UUID

from flask import render_template, flash, redirect, url_for, Blueprint, request
from flask_jwt_extended import create_access_token, decode_token
from flask_login import current_user, login_user, login_required, logout_user
from jwt import InvalidTokenError, ExpiredSignatureError, DecodeError
from werkzeug.security import check_password_hash

from src.auth.authutils import prepare_user_data, prepare_reset_psw_data
from src.auth.authwtforms import LoginForm, RegistrationForm, PasswordForgotForm, PasswordResetForm
from src.config import RESET_PSW_TOKEN_EXPIRES
from src.user.userservice import get_user_by_uname_or_email_db, create_user_db, get_user_db, update_user_db
from src.utils import send_email


auth_router = Blueprint('auth',
                        __name__,
                        static_folder='static',
                        template_folder='templates',
                        url_prefix='/auth')


@auth_router.route('/login', methods=['GET', 'POST'])
def login() -> Any:
    if current_user.is_authenticated:
        return redirect(url_for('main.show_main_page'))

    form = LoginForm()
    if form.validate_on_submit():

        if user := get_user_by_uname_or_email_db(username_or_email=form.username_or_email.data):
            if check_password_hash(user.password, form.password.data):
                login_user(user=user, remember=form.remember.data)
                return redirect(url_for('main.show_main_page'))

        flash('Invalid username or email.', 'danger')
    return render_template('auth/signin.html', form=form)


@auth_router.route('/registration', methods=['GET', 'POST'])
def registration() -> Any:
    if current_user.is_authenticated:
        return redirect(url_for('main.show_main_page'))

    form = RegistrationForm()
    if form.validate_on_submit():

        user_data = prepare_user_data(form_data=form.data)
        if new_user := create_user_db(user_data=user_data):
            login_user(new_user, remember=form.remember.data)
            return redirect(url_for('main.show_main_page'))

        flash('An account with such username or email already exists.', 'danger')
    return render_template('auth/registration.html', form=form)


@auth_router.get('/logout')
@login_required
def logout() -> Any:
    logout_user()
    return redirect(url_for('main.show_main_page'))


@auth_router.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password() -> Any:
    if current_user.is_authenticated:
        return redirect(url_for('main.show_main_page'))

    form = PasswordForgotForm()
    if form.validate_on_submit():

        if user := get_user_by_uname_or_email_db(username_or_email=form.username_or_email.data):
            token = create_access_token(identity=str(user.id),
                                        expires_delta=timedelta(minutes=RESET_PSW_TOKEN_EXPIRES))
            url = request.host_url + (url_for('auth.reset_password', token=token)[1:])
            email_body = render_template('email/resetpswemail.html', user=user, url=url)
            send_email.delay(email_subject='(Flask Blog) Reset your password',
                             email_receivers=[user.email],
                             email_body=email_body)
            flash('Further instructions have been sent to your email address.', 'primary')
            return redirect(url_for('auth.login'))

        flash('Invalid email address.', 'danger')
    return render_template('auth/forgotpassword.html', form=form)


@auth_router.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token: str) -> Any:
    if current_user.is_authenticated:
        return redirect(url_for('main.show_main_page'))

    try:
        user_id = decode_token(encoded_token=token)['sub']
        user = get_user_db(user_id=UUID(user_id))
        if not user:
            raise InvalidTokenError

    except ExpiredSignatureError:
        flash('Expired token.', 'danger')
        return redirect(url_for('auth.forgot_password'))

    except (DecodeError, InvalidTokenError, KeyError, ValueError):
        flash('Invalid token.', 'danger')
        return redirect(url_for('auth.forgot_password'))

    form = PasswordResetForm()
    if form.validate_on_submit():
        upd_psw_data = prepare_reset_psw_data(password=form.password.data)
        update_user_db(user=user, upd_data=upd_psw_data)
        email_body = render_template('email/infopswemail.html',
                                     user=user,
                                     url=request.host_url + 'forgot_password')
        send_email.delay(email_subject='(Flask Blog) Your password was reset',
                         email_receivers=[user.email],
                         email_body=email_body)
        flash('The new password has been confirmed.', 'primary')
        return redirect(url_for('auth.login'))

    return render_template('auth/newpassword.html', form=form, token=token)
