from flask_wtf import FlaskForm, RecaptchaField, Recaptcha
from wtforms import StringField, SubmitField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Regexp


class LoginForm(FlaskForm):
    username_or_email = StringField('Username or email address',
                                    validators=[DataRequired(),
                                                Length(min=6, max=100)])
    password = PasswordField('Password',
                             validators=[DataRequired(),
                                         Length(min=6, max=100)])
    remember = BooleanField('Remember me', default=False)
    recaptcha = RecaptchaField(validators=[Recaptcha(message='Invalid recaptcha')])
    submit = SubmitField('Login')


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(),
                                       Regexp(regex=r'^\w+$',
                                              message="Username must contain only letters, numbers or underscore"),
                                       Length(min=6,
                                              max=100,
                                              message='Username must be between 6 and 100 characters long')])
    email = StringField('Email address',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             validators=[DataRequired(),
                                         # Regexp(regex=r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{6,100}$',
                                         #        message='Password must contain uppercase, lowercase letters and numbers'),
                                         Length(min=6,
                                                max=100,
                                                message='Password must be between 6 and 100 characters long')])
    repeat_password = PasswordField('Confirm password',
                                    validators=[DataRequired(),
                                                EqualTo('password',
                                                        message='Password mismatch.')])
    remember = BooleanField('Remember me', default=False)
    recaptcha = RecaptchaField(validators=[Recaptcha(message='Invalid recaptcha.')])
    submit = SubmitField('Sign up')


class PasswordForgotForm(FlaskForm):
    username_or_email = StringField('Username or email address',
                                    validators=[DataRequired(), Length(min=6, max=100)])
    recaptcha = RecaptchaField(validators=[Recaptcha(message='Invalid recaptcha')])
    submit = SubmitField('Send password reset email')


class PasswordResetForm(FlaskForm):
    password = PasswordField('New password',
                             validators=[DataRequired(),
                                         # Regexp(regex=r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{6,100}$',
                                         #        message='Password must contain uppercase, lowercase letters and numbers'),
                                         Length(min=6,
                                                max=100,
                                                message='Password must be between 6 and 100 characters long')])
    repeat_password = PasswordField('Confirm new password',
                                    validators=[DataRequired(),
                                                EqualTo('password',
                                                        message='Password mismatch')])
    submit = SubmitField('Reset password')
