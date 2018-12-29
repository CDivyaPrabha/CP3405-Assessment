from flask_wtf import FlaskForm, widgets
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField, RadioField, TextAreaField, SelectField
from wtforms.widgets import TextArea
from wtforms.widgets.core import CheckboxInput, ListWidget
from wtforms.validators import DataRequired, Email, Length, InputRequired
from werkzeug.security import generate_password_hash, check_password_hash


class SignUpForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    designation = RadioField('You are a', choices=[('1', 'Student'), ('2', 'Employer')])
    checkbox = BooleanField('I agree to the given terms and conditions')
    submit = SubmitField('Create Account')


class StudentLoginForm(FlaskForm):
    student_username = StringField('Username', validators=[DataRequired()])
    student_password = PasswordField('Password', validators=[DataRequired()])
    student_submit = SubmitField('Sign In')


class EmployerLoginForm(FlaskForm):
    employer_username = StringField('Username', validators=[DataRequired()])
    employer_password = PasswordField('Password', validators=[DataRequired()])
    employer_submit = SubmitField('Sign In')


# class JobForm(FlaskForm):
#     company_name = StringField('Company\'s name', validators=[DataRequired()])
#     company_picture = FileField('Picture', validators=[FileAllowed(['jpg', 'png'], 'Images only!'), FileRequired(u'File was empty!')])
#     job_description = TextAreaField('Description', validators=[DataRequired()])
#     job_type = SelectField('Type of Job', choices=['Full-time job', 'Part-time job', 'Contract-based job'])
#     job_requirements = TextAreaField('Requirements', validators=[DataRequired()])


class User():

    def __init__(self, username):
        self.username = username
        self.email = None

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.username

    @staticmethod
    def validate_login(password_hash, password):
        return check_password_hash(password_hash, password)