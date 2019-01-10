import os
from flask import Flask

# Initialize application
app = Flask(__name__, template_folder='templates')

#Specify folder to which the uploaded images will be saved
my_path = os.path.abspath(os.path.dirname(__file__))
path = os.path.join(my_path, "static/upload_images")
UPLOAD_FOLDER = path
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# app configuration
app_settings = os.getenv(
    'APP_SETTINGS',
    'app.config.Config'
)

app.config.from_object(app_settings)
app.config.update(dict(
    SECRET_KEY="powerful secretkey",
    WTF_CSRF_SECRET_KEY="a csrf secret key"
))

from app import routes