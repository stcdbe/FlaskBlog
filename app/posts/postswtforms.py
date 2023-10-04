from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileSize, FileField, FileRequired
from wtforms import StringField, SubmitField, SelectField, TextAreaField
from wtforms.validators import Length, DataRequired


class NewsForm(FlaskForm):
    title = StringField('Title',
                        validators=[Length(min=10,
                                           max=100,
                                           message='Title must be between 5 and 100 characters long')])
    text = TextAreaField('Text',
                         validators=[Length(min=10,
                                            max=500,
                                            message='Text must be between 1 and 500 characters long')])
    category = SelectField('Category',
                           choices=[('Development', 'Development'),
                                    ('Administration', 'Administration'),
                                    ('Design', 'Design'),
                                    ('Management', 'Management'),
                                    ('Marketing', 'Marketing'),
                                    ('Science', 'Science')])
    picture = FileField('Picture in .jpg .jpeg or .png format. Max file size 10MB.',
                        validators=[FileRequired(),
                                    FileAllowed(upload_set=['jpg', 'jpeg', 'png'],
                                                message='Only pictures in .jpg .jpeg or .png format'),
                                    FileSize(max_size=10 * 1024 * 1024,
                                             message='Image size 10MB max')])
    submit = SubmitField()


class ArticleForm(NewsForm):
    intro = TextAreaField('Intro',
                          validators=[Length(max=300,
                                             message='Intro cannot be longer than 300 characters')])
    text = TextAreaField('Text',
                         validators=[Length(min=10,
                                            max=5000,
                                            message='Text must be between 1 and 5000 characters long')])


class EditNewsForm(NewsForm):
    picture = FileField('Picture in .jpg .jpeg or .png format. Max file size 10MB.',
                        validators=[FileAllowed(upload_set=['jpg', 'jpeg', 'png'],
                                                message='Only pictures in .jpg .jpeg or .png format'),
                                    FileSize(max_size=10 * 1024 * 1024,
                                             message='Image size 10MB max.')])


class EditArticleForm(ArticleForm):
    picture = FileField('Picture in .jpg .jpeg or .png format. Max file size 10MB.',
                        validators=[FileAllowed(upload_set=['jpg', 'jpeg', 'png'],
                                                message='Only pictures in .jpg .jpeg or .png format'),
                                    FileSize(max_size=10 * 1024 * 1024,
                                             message='Image size 10MB max.')])


class ArticleCommentForm(FlaskForm):
    text = TextAreaField('Commentary',
                         validators=[DataRequired(message='Commentary field is empty.'),
                                     Length(max=250,
                                            message='Commentary cannot be longer than 250 characters')])
    submit = SubmitField()
