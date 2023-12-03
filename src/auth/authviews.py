from typing import Any
from uuid import UUID

from flask import render_template, flash, redirect, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import current_user, login_user, login_required, logout_user

from src import app, db, login_manager
from src.database.dbmodels import User
from src.user.userservice import get_user_by_username_or_email_db, create_user_db
from src.auth.authwtforms import LoginForm, RegistrationForm


@login_manager.user_loader
def load_user(user_id: str | UUID) -> Any:
    return db.session.get(User, user_id)


@app.route('/signin', methods=['GET', 'POST'])
def signin() -> Any:
    if current_user.is_authenticated:
        return redirect(url_for('show_main_page'))

    form = LoginForm()
    if form.validate_on_submit():

        if check_user := get_user_by_username_or_email_db(username_or_email=form.username_or_email.data):
            if check_password_hash(check_user.password, form.password.data):
                login_user(user=check_user, remember=form.remember.data)
                return redirect(url_for('show_main_page'))
        flash('Invalid username or password.', 'danger')

    return render_template('auth/signin.html', form=form)


@app.route('/registration', methods=['GET', 'POST'])
def registration() -> Any:
    if current_user.is_authenticated:
        return redirect(url_for('show_main_page'))

    form = RegistrationForm()
    if form.validate_on_submit():

        hashed_psw = generate_password_hash(password=form.password.data, method='pbkdf2:sha512')
        user_data = {'username': form.username.data,
                     'email': form.email.data.lower(),
                     'password': hashed_psw}

        if new_user := create_user_db(user_data=user_data):
            login_user(new_user, remember=form.remember.data)
            return redirect(url_for('show_main_page'))
        flash('An account with such username or email already exists.', 'danger')

    return render_template('auth/registration.html', form=form)


@app.get('/logout')
@login_required
def logout() -> Any:
    logout_user()
    return redirect(url_for('show_main_page'))
