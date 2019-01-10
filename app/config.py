import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    DEBUG = True
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
    my_path = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(my_path, "static/upload_images")
    UPLOAD_FOLDER = path
    MLABURI = "mongodb://DivyaPrabha:practicala4@ds031972.mlab.com:31972/jcuconnect"
    MLABDB1 = "User"
    MLABDB2 = "Job"
    MLABDB3 = "CV"
    MLABDB4 = "JobCV"