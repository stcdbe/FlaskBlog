from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField, FileSize
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import URL, Length, Optional


class ProfileUpdateForm(FlaskForm):
    picture = FileField(
        label="Profile picture in .jpg, .jpeg or .png format. Max file size 16MB.",
        validators=[
            FileAllowed(["jpg", "jpeg", "png"]),
            FileSize(max_size=16 * 1024 * 1024, message="Image size 16MB max"),
        ],
    )
    fullname = StringField(
        label="Full Name",
        validators=[Optional(), Length(max=50, message="Full name cannot be longer than 50 characters.")],
        filters=[lambda x: x or None],
    )
    job_title = StringField(
        label="Job Title",
        validators=[Optional(), Length(max=50, message="Position cannot be longer than 50 characters.")],
        filters=[lambda x: x or None],
    )
    company = StringField(
        label="Company",
        validators=[Optional(), Length(max=50, message="Company cannot be longer than 50 characters.")],
        filters=[lambda x: x or None],
    )
    location = StringField(
        label="Location",
        validators=[Optional(), Length(max=50, message="Location cannot be longer than 50 characters.")],
        filters=[lambda x: x or None],
    )
    website = URLField(
        label="Website",
        validators=[Optional(), URL(message="Website link must be URL.")],
        filters=[lambda x: x or None],
    )
    github = StringField(
        label="Github",
        validators=[Optional(), URL(message="Github link must be URL.")],
        filters=[lambda x: x or None],
    )
    twitter = StringField(
        label="Twitter",
        validators=[Optional(), URL(message="Twitter link must be URL.")],
        filters=[lambda x: x or None],
    )
    submit = SubmitField(label="Save Changes")
