from ..models import User
from flask_wtf import FlaskForm
from wtforms import \
    StringField, PasswordField, BooleanField, SubmitField, ValidationError
from wtforms.validators import \
    DataRequired, Length, Email, Regexp, EqualTo


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('Senha', validators=[DataRequired()])
    remember_me = BooleanField('Mantenha me logado')
    submit = SubmitField('Acessar')


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1,64), Email()])
    username = StringField('Usuário', validators=[
        DataRequired(),
        Length(1,64),
        Regexp(
            '^[A-Za-z][A-Za-z0-9_.]*$',
            0,
            'Usuário deve ter somente letras, numeros, ponto ou undescore'
        )])
    password = PasswordField('Senha', validators=[
        DataRequired(),
        EqualTo('confirm_password', message='Senha não corresponde')
    ])
    confirm_password = PasswordField('Conrime a senha', validators=[DataRequired()])
    submit = SubmitField('Registrar')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email já cadastrado')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Usuario já cadastrado')
