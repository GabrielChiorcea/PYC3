from flask import flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, validators, ValidationError
from wtforms.validators import DataRequired, Length


class Create(FlaskForm):
    name = StringField('Name',  [validators.DataRequired(), Length(min=4, max=20)])
    password = PasswordField('Password' , [validators.DataRequired()])
    submit = SubmitField('Submit')

    def validate_username(self, field):
        if (field):
            raise ValidationError('Numele exista deja.')





class SingUp (FlaskForm):
    name = StringField('Name' , [validators.DataRequired(), Length(min=4, max=20)])
    password = PasswordField('Password' , [validators.DataRequired()])
    submit = SubmitField('Submit')

    def validate_user(self, field):
        if (field):
            raise ValidationError('User sau parola incorecte')

    



