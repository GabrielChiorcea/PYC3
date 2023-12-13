from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

class MyForm(FlaskForm):
    name = StringField('Name')
    prename = StringField('PreName')
    submit = SubmitField('Submit')



class SingUp (FlaskForm):
    name = StringField('Name')
    prename = StringField('PreName')
    submit = SubmitField('Submit')