from flask import flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, validators, ValidationError
from wtforms.validators import DataRequired, Length, Regexp

class CreateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=6, message="Parola trebuie să aibă minim 6 caractere."),
        Regexp('^[A-Za-z]+$', message="Parola trebuie să conțină doar litere.")
    ])

class Create(FlaskForm):
    name = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=6, message="Parola trebuie să aibă minim 6 caractere."),
        Regexp('^[A-Za-z]+$', message="Parola trebuie să conțină doar litere.")
    ])

class SingUp (FlaskForm):
    name = StringField('Name' , [validators.DataRequired(), Length(min=4, max=20)])
    password = PasswordField('Password' , [validators.DataRequired()])
    submit = SubmitField('Submit')

    def validate_user(self, field):
        if (field):
            raise ValidationError('User sau parola incorecte')

