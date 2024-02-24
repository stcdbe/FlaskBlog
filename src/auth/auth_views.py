from flask import render_template, flash, redirect, url_for, Blueprint, Response
from flask_login import current_user, login_required
from injector import inject

from src.auth.auth_services import AuthService
from src.auth.auth_wtforms import LoginForm, RegistrationForm, PasswordForgotForm, PasswordResetForm
from src.user.user_exceptions import InvalidUserDataError

auth_router = Blueprint(name='auth',
                        import_name=__name__,
                        static_folder='static',
                        template_folder='templates',
                        url_prefix='/auth')


@auth_router.route(rule='/login', methods=['GET', 'POST'])
@inject
def login(auth_service: AuthService) -> Response | str:
    if current_user.is_authenticated:
        return redirect(url_for('main.show_main_page'))

    form = LoginForm()
    if form.validate_on_submit():
        try:
            auth_service.login(login_data=form.data)

        except InvalidUserDataError as exc:
            flash(f'{exc}', 'danger')

        else:
            return redirect(url_for('main.show_main_page'))

    return render_template('auth/login.html', form=form)


@auth_router.route(rule='/registration', methods=['GET', 'POST'])
@inject
def registration(auth_service: AuthService) -> Response | str:
    if current_user.is_authenticated:
        return redirect(url_for('main.show_main_page'))

    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            auth_service.registrate(user_data=form.data)

        except InvalidUserDataError as exc:
            flash(f'{exc}', 'danger')

        else:
            return redirect(url_for('main.show_main_page'))

    return render_template('auth/registration.html', form=form)


@auth_router.get(rule='/logout')
@login_required
@inject
def logout(auth_service: AuthService) -> Response:
    auth_service.logout()
    return redirect(url_for('main.show_main_page'))


@auth_router.route(rule='/forgot_password', methods=['GET', 'POST'])
@inject
def forgot_password(auth_service: AuthService) -> Response | str:
    if current_user.is_authenticated:
        return redirect(url_for('main.show_main_page'))

    form = PasswordForgotForm()
    if form.validate_on_submit():
        try:
            auth_service.forgot_psw(email=form.email.data)

        except InvalidUserDataError as exc:
            flash(f'{exc}', 'danger')

        else:
            flash('Further instructions have been sent to your email address.', 'primary')
            return redirect(url_for('auth.login'))

    return render_template('auth/forgot_password.html', form=form)


@auth_router.route(rule='/reset_password/<token>', methods=['GET', 'POST'])
@inject
def reset_password(auth_service: AuthService, token: str) -> Response | str:
    if current_user.is_authenticated:
        return redirect(url_for('main.show_main_page'))

    try:
        user = auth_service.validate_token(token=token)

    except InvalidUserDataError as exc:
        flash(f'{exc}', 'danger')
        return redirect(url_for('auth.forgot_password'))

    form = PasswordResetForm()
    if form.validate_on_submit():
        auth_service.reset_psw(user=user, new_password=form.password.data)
        flash('The new password has been confirmed.', 'primary')
        return redirect(url_for('auth.login'))

    return render_template('auth/reset_password.html', form=form, token=token)
