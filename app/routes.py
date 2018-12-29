from flask import render_template, flash, redirect, request, url_for
from app import app
from app.forms import SignUpForm, StudentLoginForm, EmployerLoginForm, User, JobForm
from pymongo import MongoClient
from werkzeug.security import generate_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user


client = MongoClient("mongodb://DivyaPrabha:practicala4@ds031972.mlab.com:31972/jcuconnect")
user_collection = client["jcuconnect"].User
job_collection = client["jcuconnect"].Job

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user):
    u = user_collection.find_one({"Username": user})
    if not u:
        return None
    return User(u['Username'])


@app.route('/')
@app.route('/index')
def index():
    if current_user.is_authenticated:
        user = current_user
    else:
        user = "guest"
    posts = user_collection.find()

    return render_template('index.html', title='Home', user=user, posts=posts)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if request.method == 'POST' and form.validate_on_submit():
        # check if user_name or email is taken
        user = user_collection.find_one({"Username": form.username.data})
        if user and User.validate_login(user['Password'], form.password.data):
            flash("User already exists!", category='error')
            return render_template('signup.html', title='signup', form=form)
        pass_hash = generate_password_hash(form.password.data, method='pbkdf2:sha256')
        post_data = {
            'Username': form.username.data,
            'Password': pass_hash,
            'Email': form.email.data,
            'Designation': form.designation.data,
            'Checkbox': form.checkbox.data
        }
        user_collection.insert_one(post_data)
        # log the user in
        user = user_collection.find_one({"Username": form.username.data})
        user_obj = User(user['Username'])
        login_user(user_obj)
        flash("Logged in successfully!", category='success')
        return "<h1>Signed in successfully!"#go to student/employer home page
    return render_template('signup.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    student_form = StudentLoginForm()
    employer_form = EmployerLoginForm()
    if request.method == 'POST':
        if student_form.validate_on_submit() and student_form.student_submit.data:
            user = user_collection.find_one({"Username": student_form.student_username.data})
            print(user)
            if user and User.validate_login(user['Password'], student_form.student_password.data):
                user_obj = User(user['Username'])
                login_user(user_obj)
                flash("Logged in successfully!", category='success')
                return "<h1>Signed in successfully!"# go to student home page
            flash("Wrong username or password!", category='error')
        elif employer_form.validate_on_submit() and employer_form.employer_submit.data:
            user = user_collection.find_one({"Username": employer_form.employer_username.data})
            if user and User.validate_login(user['Password'], employer_form.employer_password.data):
                user_obj = User(user['Username'])
                login_user(user_obj)
                flash("Logged in successfully!", category='success')
                return "<h1>Signed in successfully!"# go to employer home page
            flash("Wrong username or password!", category='error')
    return render_template('login.html', title='login', student_form=student_form, employer_form=employer_form)


# @app.route('/postjob', methods=['GET', 'POST'])
# def postjob():
#     form = JobForm()
#     if form.validate_on_submit():
#         picture_name = form.company_picture.data.filename
#         form.company_picture.data.save('static/upload_images/' + picture_name)
#         picture_path =
#         post_data = {
#             'Company Name': form.company_name.data
#             'Company Picture': form.
#         }


@app.route('/logout', methods = ['GET'])
@login_required
def logout():
    logout_user()
    client.close()
    return redirect(url_for('login'))