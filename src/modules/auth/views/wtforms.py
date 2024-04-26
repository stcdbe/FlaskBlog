from flask_wtf import FlaskForm, Recaptcha, RecaptchaField
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Regexp


class LoginForm(FlaskForm):
    username_or_email = StringField(
        label="Username or email address",
        validators=[DataRequired(), Length(min=6, max=100)],
    )
    password = PasswordField(label="Password", validators=[DataRequired(), Length(min=6, max=72)])
    remember = BooleanField(label="Remember me", default=False)
    recaptcha = RecaptchaField(validators=[Recaptcha(message="Invalid recaptcha")])
    submit = SubmitField(label="Sign in")


class RegistrationForm(FlaskForm):
    username = StringField(
        label="Username",
        validators=[
            DataRequired(),
            Regexp(regex=r"^\w+$", message="Username must contain only letters, numbers or underscore"),
            Length(min=6, max=100, message="Username must be between 6 and 100 characters long"),
        ],
    )
    email = StringField(label="Email address", validators=[DataRequired(), Email()])
    password = PasswordField(
        label="Password",
        validators=[
            DataRequired(),
            Regexp(
                regex=r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9]).{10,72}$",
                message="Password must contain uppercase, lowercase letters and numbers",
            ),
            Length(min=10, max=72, message="Password must be between 6 and 100 characters long"),
        ],
    )
    repeat_password = PasswordField(
        label="Confirm password",
        validators=[DataRequired(), EqualTo("password", message="Password mismatch.")],
    )
    remember = BooleanField(label="Remember me", default=False)
    recaptcha = RecaptchaField(validators=[Recaptcha(message="Invalid recaptcha.")])
    submit = SubmitField(label="Sign up")


class PasswordForgotForm(FlaskForm):
    email = StringField(label="Email address", validators=[DataRequired(), Email()])
    recaptcha = RecaptchaField(validators=[Recaptcha(message="Invalid recaptcha")])
    submit = SubmitField(label="Send password reset email")


class PasswordResetForm(FlaskForm):
    password = PasswordField(
        label="New password",
        validators=[
            DataRequired(),
            Regexp(
                regex=r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9]).{10,72}$",
                message="Password must contain uppercase, lowercase letters and numbers",
            ),
            Length(min=10, max=72, message="Password must be between 6 and 100 characters long"),
        ],
    )
    repeat_password = PasswordField(
        label="Confirm new password",
        validators=[DataRequired(), EqualTo("password", message="Password mismatch")],
    )
    submit = SubmitField(label="Reset password")
