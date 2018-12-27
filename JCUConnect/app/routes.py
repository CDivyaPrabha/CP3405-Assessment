from flask import render_template, flash, redirect, request, url_for
from app import app
from app.forms import SignUpForm
from pymongo import MongoClient
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user


client = MongoClient("mongodb://DivyaPrabha:practicala4@ds031972.mlab.com:31972/jcuconnect")
collection = client["jcuconnect"].User

#login_manager = LoginManager()
#login_manager.init_app(app)


#@app.route('/')
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        post_data = {
            'Username': form.username.data,
            'Password': form.password.data,
            'Email': form.email.data,
            'Designation': form.designation.data,
            'Remember user': form.remember_me.data,
            'Checkbox': form.checkbox.data
        }
        result = collection.insert_one(post_data)
    return render_template('signup.html', form=form)