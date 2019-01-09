import os
from flask import render_template, flash, redirect, request, send_from_directory, url_for
from app import app
from app.forms import SignUpForm, StudentLoginForm, EmployerLoginForm, User, JobForm, CVForm
from pymongo import MongoClient
from werkzeug.security import generate_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.utils import secure_filename
from bson import ObjectId


client = MongoClient("mongodb://DivyaPrabha:practicala4@ds031972.mlab.com:31972/jcuconnect")
user_collection = client["jcuconnect"].User
job_collection = client["jcuconnect"].Job
cv_collection = client["jcuconnect"].CV
jobcv_collection = client["jcuconnect"].JobCV

global user_name

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


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
        # make user_name global to be shared by all functions
        global user_name
        user_name = form.username.data
        if user['Designation']=="1":
            return redirect(url_for('student_home_page'))  # go to student home page
        elif user['Designation']=="2":
            return redirect(url_for('employer_home_page'))  # go to employer home page
    return render_template('signup.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    student_form = StudentLoginForm()
    employer_form = EmployerLoginForm()
    global user_name

    if request.method == 'POST':

        # log the student in
        if student_form.validate_on_submit() and student_form.student_submit.data:
            user = user_collection.find_one({"Username": student_form.student_username.data})
            if user and User.validate_login(user['Password'], student_form.student_password.data) and user['Designation']=="1":
                user_obj = User(user['Username'])
                login_user(user_obj)
                flash("Logged in successfully!", category='success')
                user_name = student_form.student_username.data
                return redirect(url_for('student_home_page'))  # go to student home page
            flash("Wrong username or password!", category='error')

        # log the employer in
        elif employer_form.validate_on_submit() and employer_form.employer_submit.data:
            user = user_collection.find_one({"Username": employer_form.employer_username.data})
            if user and User.validate_login(user['Password'], employer_form.employer_password.data) and user['Designation']=="2":
                user_obj = User(user['Username'])
                login_user(user_obj)
                flash("Logged in successfully!", category='success')
                user_name = employer_form.employer_username.data
                return redirect(url_for('employer_home_page'))  # go to employer home page
            flash("Wrong username or password!", category='error')

    return render_template('login.html', title='login', student_form=student_form, employer_form=employer_form)


@app.route('/employer_home_page')
def employer_home_page():
    CVs = []

    # find current user _id
    user = user_collection.find_one({"Username": user_name})
    user_id = user['_id']

    # find jobs posted by current employer
    jobs = job_collection.find({"Employer_ID": user_id})
    for job in jobs:
        job_id = ObjectId(job['_id'])
        posts = jobcv_collection.find({"Job_ID": job_id})
        for post in posts:
            # find CVs for the applicants who applied for this job
            cv = cv_collection.find_one({"_id": post["CV_ID"]})
            cv['Job_Designation'] = job['Job_Designation']
            CVs.append(cv)
    return render_template('employer_home.html', CVs=CVs)


@app.route('/display_employer_jobs')
def display_employer_jobs():
    # find current user _id
    user = user_collection.find_one({"Username": user_name})
    user_id = user['_id']

    # find jobs posted by current user
    posts = job_collection.find({"Employer_ID": user_id})
    return render_template('posting_jobs.html', posts=posts)


@app.route('/postjob', methods=['GET', 'POST'])
def postjob():
    form = JobForm()
    if request.method == 'POST' and form.validate_on_submit():

        # check if uploaded image is png, jpeg or jpg type
        if allowed_file(form.company_picture.data.filename):
            picture_name = secure_filename(form.company_picture.data.filename)
            # save uploaded picture to directory upload_images in static directory
            form.company_picture.data.save(os.path.join(app.config['UPLOAD_FOLDER'], picture_name))
            # create a path to picture to store in database
            picture_name = "../static/upload_images/" + picture_name
            job_type = request.form['job_type']
            user = user_collection.find_one({"Username": user_name})
            user_id = user['_id']
            post_data = {
                'Company_Name': form.company_name.data,
                'Job_Designation': form.job_designation.data,
                'Company_Picture': picture_name,
                'Job_Description': form.job_description.data,
                'Job_Type': job_type,
                'Job_Requirements': form.job_requirements.data,
                'Employer_ID': user_id
            }
            job_collection.insert_one(post_data)
            return redirect(url_for('display_employer_jobs'))
    return render_template('form_page.html', form=form)


def allowed_file(filename):
    # check if filename is of png, jpeg or jpg type
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/student_home_page')
def student_home_page():
    return render_template('homeStudent.html')


@app.route('/student_jobs')
def student_jobs():
    jobs = job_collection.find()
    user = user_collection.find_one({"Username": user_name})
    user_id = user['_id']
    # find CV for current student id
    cv = cv_collection.find_one({"Student_ID": user_id})
    if cv is not None:
        jobs = []
        cv_id = cv['_id']
        posts = job_collection.find()
        for job in posts:
            job_id = job['_id']
            temp_jobs = jobcv_collection.find({"Job_ID": job_id})
            for temp_job in temp_jobs:
                # check if the student has already applied to the job
                if temp_job['CV_ID'] == cv_id:
                    job['Applied'] = "Yes"
                else:
                    job['Applied'] = "No"
            jobs.append(job)
    return render_template('searchJob.html', jobs=jobs)


@app.route('/redirect_cv')
def redirect_cv():
    user = user_collection.find_one({"Username": user_name})
    user_id = user['_id']
    post = cv_collection.find_one({"Student_ID": user_id})
    if post is None:
        return redirect(url_for('cv_form'))  # redirect to CV form if user does not have a CV yet
    else:
        return redirect(url_for('centralisedCV'))  # redirect to CV page if user already has a CV


@app.route('/cv_form', methods=['GET', 'POST'])
def cv_form():
    form = CVForm()
    if request.method == "POST" and form.validate_on_submit():
        user = user_collection.find_one({"Username": user_name})
        user_id = user['_id']
        # check if uploaded image is png, jpeg or jpg type
        if allowed_file(form.student_picture.data.filename):
            picture_name = secure_filename(form.student_picture.data.filename)
            # save uploaded picture to directory upload_images in static directory
            form.student_picture.data.save(os.path.join(app.config['UPLOAD_FOLDER'], picture_name))
            # create a path to picture to store in database
            picture_name = "../static/upload_images/" + picture_name
            post_data = {
                'Student_picture': picture_name,
                'Student_name': form.student_name.data,
                'Student_phone': form.student_phone.data,
                'Student_mobile': form.student_mobile.data,
                'Student_email': form.student_email.data,
                'Student_address': form.student_address.data,
            
                'Student_education': form.student_education.data,
                'Student_major': form.student_major.data,
                'Student_university': form.student_university.data,
                'Student_university_country': form.student_university_country.data,
                'Student_graduate_year': form.student_graduate_year.data,
            
                'Student_work_experience': form.student_work_experience.data,
                'Student_projects': form.student_projects.data,
                'Student_workshops': form.student_workshops.data,
            
                'Student_skills': form.student_skills.data,
                'Student_interests': form.student_interests.data,
            
                'Student_ID': user_id
            }
            cv_collection.insert_one(post_data)
            return redirect(url_for('centralisedCV'))
    return render_template('formCV.html', form=form)


@app.route('/centralisedCV')
def centralisedCV():
    # find cv according to student id
    user = user_collection.find_one({"Username": user_name})
    user_id = user['_id']
    post = cv_collection.find_one({"Student_ID": user_id})
    return render_template('centralisedCV.html', post=post)


@app.route('/apply_for_job/<job_id>')
def apply_for_job(job_id):
    # find job according to job id
    job_object_id = ObjectId(job_id)
    post = job_collection.find_one({"_id": job_object_id})
    return render_template('apply_jobs.html', post=post)


@app.route('/sendCV/<job_id>')
def sendCV(job_id):
    user = user_collection.find_one({"Username": user_name})
    user_id = user['_id']
    # find CV according to student id
    cv = cv_collection.find_one({"Student_ID": user_id})
    cv_id = cv['_id']
    job_object_id = ObjectId(job_id)
    # link the job id and cv id in a document after applying for a job
    post_data = {
        "Job_ID": job_object_id,
        "CV_ID": cv_id
    }
    jobcv_collection.insert_one(post_data)
    return redirect(url_for('student_jobs'))


@app.route('/viewCV/<cv_id>')
def viewCV(cv_id):
    # find CV according to CV id
    cv_object_id = ObjectId(cv_id)
    post = cv_collection.find_one({"_id": cv_object_id})
    return render_template('centralisedCV.html', post=post)


@app.route('/logout', methods=['GET'])
@login_required
def logout():
    # log the user out
    logout_user()
    client.close()
    global user_name
    user_name=None
    return redirect(url_for('login'))