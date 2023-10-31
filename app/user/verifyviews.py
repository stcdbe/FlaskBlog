from uuid import UUID

from flask import render_template, flash, redirect, url_for, Response
from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import current_user, login_user, login_required, logout_user

from app import app, db, login_manager
from app.database.dbmodels import User
from app.database.dbfuncs import getuser, addnewuser
from app.user.verifywtforms import LoginForm, RegistrationForm


@login_manager.user_loader
def loaduser(id: UUID) -> User:
    user = db.session.get(User, id)
    return user


@app.route('/signin', methods=['GET', 'POST'])
def signin() -> str | Response:
    if current_user.is_authenticated:
        return redirect(url_for('main'))

    form = LoginForm()
    if form.validate_on_submit():
        checkuser = getuser(usernameoremail=form.usernameoremail.data)
        if checkuser:
            checkpsw = check_password_hash(checkuser.password, form.password.data)
            if checkpsw:
                rm = form.remember.data
                login_user(user=checkuser, remember=rm)
                return redirect(url_for('main'))
            else:
                flash('Invalid username or password.', 'danger')
        else:
            flash('Invalid username or password.', 'danger')

    return render_template('verification/signin.html', form=form)


@app.route('/registration', methods=['GET', 'POST'])
def registration() -> str | Response:
    if current_user.is_authenticated:
        return redirect(url_for('main'))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashedpsw = generate_password_hash(password=form.password.data,
                                           method='pbkdf2:sha512')
        userdata = {'username': form.username.data,
                    'email': form.email.data,
                    'password': hashedpsw}
        try:
            newuser = addnewuser(userdata=userdata)
            rm = form.remember.data
            login_user(newuser, remember=rm)
            return redirect(url_for(endpoint='showposts', posts='articles'))
        except IntegrityError:
            flash('An account with such username or email already exists.', 'danger')

    return render_template('verification/registration.html', form=form)


@app.route('/logout')
@login_required
def logout() -> Response:
    logout_user()
    return redirect(url_for('main'))
