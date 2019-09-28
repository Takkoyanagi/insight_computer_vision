import os
from flask import Flask
from flask_mobility import Mobility
from flask_app import static

# # set path to templates
# template_dir = os.getcwd()
# template_dir = os.path.join(template_dir, 'templates')

# initialize our Flask application and the Keras model
# app = Flask(__name__, template_folder=template_dir)
app = Flask(__name__)

Mobility(app)

UPLOAD_FOLDER = './uploads'

with open('flask_app/static/secret_code.txt', 'r') as f:
    sw = f.read()

app.secret_key = sw
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

from flask_app import views
