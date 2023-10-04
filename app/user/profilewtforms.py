from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileSize
from wtforms import StringField, URLField, SubmitField
from wtforms.validators import Length, Optional, URL


class EditProfileForm(FlaskForm):
    picture = FileField('Profile picture in .jpg, .jpeg or .png format',
                        validators=[FileAllowed(['jpg', 'jpeg', 'png']),
                                    FileSize(max_size=10 * 1024 * 1024)])
    name = StringField('Full Name',
                       validators=[Length(max=50,
                                          message='Full name cannot be longer than 50 characters.')])
    position = StringField('Position',
                           validators=[Length(max=100,
                                              message='Position cannot be longer than 100 characters.')])
    company = StringField('Company',
                          validators=[Length(max=50,
                                             message='Company cannot be longer than 50 characters.')])
    location = StringField('Location',
                           validators=[Length(max=50,
                                              message='Location cannot be longer than 50 characters.')])
    website = URLField('Website',
                       validators=[Optional(),
                                   URL(require_tld=True,
                                       message='Website link must be URL.')])
    github = StringField('Github',
                         validators=[Optional(),
                                     URL(require_tld=True,
                                         message='Github link must be URL.')])
    twitter = StringField('Twitter',
                          validators=[Optional(),
                                      URL(require_tld=True,
                                          message='Twitter link must be URL.')])
    submit = SubmitField('Save Changes')
