from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileSize
from wtforms import StringField, URLField, SubmitField
from wtforms.validators import Length, Optional, URL


class ProfileUpdateForm(FlaskForm):
    picture = FileField('Profile picture in .jpg, .jpeg or .png format. Max file size 16MB.',
                        validators=[FileAllowed(['jpg', 'jpeg', 'png']),
                                    FileSize(max_size=16 * 1024 * 1024, message='Image size 16MB max')])
    fullname = StringField('Full Name',
                           validators=[Optional(),
                                       Length(max=50,
                                              message='Full name cannot be longer than 50 characters.')],
                           filters=[lambda x: x or None])
    job_title = StringField('Job Title',
                            validators=[Optional(),
                                        Length(max=50,
                                               message='Position cannot be longer than 50 characters.')],
                            filters=[lambda x: x or None])
    company = StringField('Company',
                          validators=[Optional(),
                                      Length(max=50,
                                             message='Company cannot be longer than 50 characters.')],
                          filters=[lambda x: x or None])
    location = StringField('Location',
                           validators=[Optional(),
                                       Length(max=50,
                                              message='Location cannot be longer than 50 characters.')],
                           filters=[lambda x: x or None])
    website = URLField('Website',
                       validators=[Optional(),
                                   URL(message='Website link must be URL.')],
                       filters=[lambda x: x or None])
    github = StringField('Github',
                         validators=[Optional(),
                                     URL(message='Github link must be URL.')],
                         filters=[lambda x: x or None])
    twitter = StringField('Twitter',
                          validators=[Optional(),
                                      URL(message='Twitter link must be URL.')],
                          filters=[lambda x: x or None])
    submit = SubmitField('Save Changes')
