from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField, FileRequired, FileSize
from wtforms import SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Optional

from src.modules.post.models.enums import PostCategory, PostGroup


class PostCreateForm(FlaskForm):
    title = StringField(
        label="Title",
        validators=[
            DataRequired(message="Title field is empty"),
            Length(min=10, max=100, message="Title must be between 10 and 100 characters long"),
        ],
    )
    intro = TextAreaField(
        label="Intro",
        validators=[Optional(), Length(max=300, message="Intro cannot be longer than 300 characters")],
        filters=[lambda x: x or None],
    )
    text = TextAreaField(
        label="Text",
        validators=[
            DataRequired(message="Text field is empty."),
            Length(min=10, message="Text cannot be shorter than 10 characters"),
        ],
    )
    group = SelectField(
        label="Post group",
        choices=[
            (
                choice,
                choice.capitalize(),
            )
            for choice in PostGroup
        ],
    )
    category = SelectField(
        label="Category",
        choices=[
            (
                choice,
                choice.capitalize(),
            )
            for choice in PostCategory
        ],
    )
    picture = FileField(
        label="Picture in .jpg .jpeg or .png format. Max file size 16MB.",
        validators=[
            FileRequired(),
            FileAllowed(upload_set=["jpg", "jpeg", "png"], message="Only .jpg .jpeg or .png pictures"),
            FileSize(max_size=16 * 1024 * 1024, message="Image size 16MB max"),
        ],
    )
    submit = SubmitField()


class PostUpdateForm(PostCreateForm):
    picture = FileField(
        label="Picture in .jpg .jpeg or .png format. Max file size 16MB.",
        validators=[
            FileAllowed(upload_set=["jpg", "jpeg", "png"], message="Only .jpg .jpeg or .png pictures"),
            FileSize(max_size=16 * 1024 * 1024, message="Image size 16MB max."),
        ],
    )


class CommentCreateForm(FlaskForm):
    text = TextAreaField(
        label="Commentary",
        validators=[
            DataRequired(message="Commentary field is empty"),
            Length(max=250, message="Commentary cannot be longer than 250 characters"),
        ],
    )
    submit = SubmitField()
