from flask_wtf import FlaskForm, widgets
from wtforms import StringField, PasswordField, BooleanField, SubmitField, RadioField
from wtforms.widgets.core import CheckboxInput, ListWidget
from wtforms.validators import DataRequired, Email, Length, InputRequired
from werkzeug.security import generate_password_hash, check_password_hash


class SignUpForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    designation = RadioField('You are a', choices=[('1', 'Student'), ('2', 'Employer')])
    checkbox = BooleanField('I agree to the given terms and conditions')
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Create Account')