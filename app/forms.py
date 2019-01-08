from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField, RadioField, TextAreaField
from wtforms.validators import DataRequired, Email
from werkzeug.security import check_password_hash


class SignUpForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    email = StringField('Email', validators=[Email()])
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


class JobForm(FlaskForm):
    company_name = StringField('Company\'s Name: ', validators=[DataRequired()])
    job_designation = StringField('Job Designation: ', validators=[DataRequired()])
    company_picture = FileField('Picture: ', validators=[FileAllowed(['jpg', 'png'], 'Images only!'),
                                                       FileRequired(u'File was empty!')])
    job_description = TextAreaField('Description: ', validators=[DataRequired()], render_kw={"rows": 8, "cols": 50})
    job_requirements = TextAreaField('Requirements: ', validators=[DataRequired()], render_kw={"rows": 8, "cols": 50})
    post_job = SubmitField('Post job')


class CVForm(FlaskForm):
    student_name = StringField('Full Name: ', validators=[DataRequired()])
    student_phone = StringField('Phone: ')
    student_mobile = StringField('Mobile: ', validators=[DataRequired()])
    student_email = StringField('Email: ', validators=[DataRequired()])
    student_address = StringField('Address: ', validators=[DataRequired()])

    student_education = StringField('Education: ', validators=[DataRequired()])
    student_major = StringField('Major: ')
    student_university = StringField('University: ', validators=[DataRequired()])
    student_university_country = StringField('Country: ', validators=[DataRequired()])
    student_graduate_year = StringField('Graduate Year: ', validators=[DataRequired()])

    student_work_experience = TextAreaField('Work Experience: ', render_kw={"rows": 8, "cols": 50})
    student_projects = TextAreaField('Projects Completed: ', render_kw={"rows": 8, "cols": 50})
    student_workshops = TextAreaField('Workshops, Seminars and Training: ', render_kw={"rows": 8, "cols": 50})

    student_skills = TextAreaField('Skills: ', validators=[DataRequired()], render_kw={"rows": 8, "cols": 50})
    student_interests = TextAreaField('Interests: ', render_kw={"rows": 8, "cols": 50})

    submit_cv = SubmitField('Submit')


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