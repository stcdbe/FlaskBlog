from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileSize, FileField, FileRequired
from wtforms import StringField, SubmitField, SelectField, TextAreaField
from wtforms.validators import Length, DataRequired, Optional


class NewsPostCreateForm(FlaskForm):
    title = StringField('Title',
                        validators=[DataRequired(message='Title field is empty.'),
                                    Length(min=10,
                                           max=100,
                                           message='Title must be between 10 and 100 characters long')])
    text = TextAreaField('Text',
                         validators=[DataRequired(message='Text field is empty.'),
                                     Length(min=10,
                                            max=500,
                                            message='Text must be between 10 and 500 characters long')])
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


class ArticleCreateForm(NewsPostCreateForm):
    intro = TextAreaField('Intro',
                          validators=[Optional(),
                                      Length(max=300,
                                             message='Intro cannot be longer than 300 characters')],
                          filters=[lambda x: x or None])
    text = TextAreaField('Text',
                         validators=[DataRequired(message='Text field is empty.'),
                                     Length(min=10,
                                            max=5000,
                                            message='Text must be between 10 and 5000 characters long')])


class NewsPostUpdateForm(NewsPostCreateForm):
    picture = FileField('Picture in .jpg .jpeg or .png format. Max file size 10MB.',
                        validators=[FileAllowed(upload_set=['jpg', 'jpeg', 'png'],
                                                message='Only pictures in .jpg .jpeg or .png format'),
                                    FileSize(max_size=10 * 1024 * 1024,
                                             message='Image size 10MB max.')])


class ArticleUpdateForm(ArticleCreateForm):
    picture = FileField('Picture in .jpg .jpeg or .png format. Max file size 10MB.',
                        validators=[FileAllowed(upload_set=['jpg', 'jpeg', 'png'],
                                                message='Only pictures in .jpg .jpeg or .png format'),
                                    FileSize(max_size=10 * 1024 * 1024,
                                             message='Image size 10MB max.')])


class CommentCreateForm(FlaskForm):
    text = TextAreaField('Commentary',
                         validators=[DataRequired(message='Commentary field is empty.'),
                                     Length(max=250,
                                            message='Commentary cannot be longer than 250 characters')])
    submit = SubmitField()
