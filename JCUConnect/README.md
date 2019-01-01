Setup your account on heroku
Setup your account on mlab.com

heroku apps:create unique-name-of-your-app

create python env:
python -m venv venv

pip install gunicorn

save dependency packages
pip freeze > requirements.txt


test local
$ export FLASK_APP=main.py
$ flask run

Flask environment set as .flaskenv

Procfile contain the launch of the python application.

## MongoDB access
To access MongoDB I have created a mongodb on mlab.com

Create your account on mlab
create a db and a collection

also, create a db user and use that user in your URI
mongodb://<dbuser>:<dbpassword>@ds139675.mlab.com:39675/dbname

the setup.sh file holds the environment variables the application will use.
use source setupenv.sh to set envirnment variables

You can hardcode these variables in the config.py file

to generate the SECRET_KEY you can use gpg:

$ gpg --gen-random --armor 1 14

or

$ openssl rand -base64 14

it will generate something like this:

IFRj4uTWB2cdAd3FYhk=



