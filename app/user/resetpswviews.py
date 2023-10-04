from datetime import timedelta

from flask import redirect, url_for, request, flash, render_template, Response
from flask_jwt_extended import create_access_token, decode_token
from flask_login import current_user
from jwt import ExpiredSignatureError, DecodeError, InvalidTokenError
from werkzeug.security import generate_password_hash

from app import app
from app.user.verifywtforms import ForgotPasswordForm, ResetPasswordForm
from app.utils import sendemail
from app.database.dbfuncs import getuser, getuserbyid, adduserdata


@app.route('/forgotpassword', methods=['GET', 'POST'])
def forgotpassword() -> str | Response:
    if current_user.is_authenticated:
        return redirect(url_for('main'))

    form = ForgotPasswordForm()
    if form.validate_on_submit():
        user = getuser(usernameoremail=form.email.data)
        if user:
            token = create_access_token(identity=str(user.id),
                                        expires_delta=timedelta(hours=6))
            sendemail(subject='(Flask Blog) Reset your password',
                      user=user,
                      url=request.host_url + 'resetpassword/' + token,
                      template='resetpswemail.html')
            flash('Further instructions have been sent to your email address.', 'primary')
            return redirect(url_for('signin'))

        flash('Invalid email address.', 'danger')
    return render_template('verification/forgotpassword.html', form=form)


@app.route('/resetpassword/<token>', methods=['GET', 'POST'])
def resetpassword(token: str) -> str | Response:
    if current_user.is_authenticated:
        return redirect(url_for('main'))

    try:
        userid = decode_token(encoded_token=token)['sub']
        user = getuserbyid(id=userid)
        form = ResetPasswordForm()
        if form.validate_on_submit():
            hashedpsw = generate_password_hash(password=form.password.data, method='pbkdf2:sha512')
            adduserdata(user=user, data=dict(password=hashedpsw))
            sendemail(subject='(Flask Blog) Your password was reset',
                      user=user,
                      url=request.host_url + 'forgotpassword',
                      template='infopswemail.html')
            flash('The new password has been confirmed.', 'primary')
            return redirect(url_for('signin'))
        return render_template('verification/newpassword.html', form=form, token=token)

    except ExpiredSignatureError:
        flash('Expired token.', 'danger')
        return redirect(url_for('forgotpassword'))

    except (DecodeError, InvalidTokenError):
        flash('Invalid token.', 'danger')
        return redirect(url_for('forgotpassword'))
