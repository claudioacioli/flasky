from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length


class NameForm(FlaskForm):
    name = StringField('Qual é o seu nome:', validators=[DataRequired()])
    submit = SubmitField('Submit')


class EditProfileForm(FlaskForm):
    name = StringField('Nome:', validators=[Length(0,64)])
    location = StringField('Localização: ', validators=[Length(0,64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')
