import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    DEBUG = True
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
    UPLOAD_FOLDER = 'static/upload_images'
    MLABURI = "mongodb://DivyaPrabha:practicala4@ds031972.mlab.com:31972/jcuconnect"
    MLABDB1 = "User"
    MLABDB2 = "Job"
    MLABDB3 = "CV"