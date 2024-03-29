# import the necessary packages
from __future__ import print_function, division

import torch
import torch.nn as nn
import torch.optim as optim
from torch.optim import lr_scheduler
import numpy as np
import torchvision
from torchvision import datasets, models, transforms
import os
import io
from PIL import Image
from flask import render_template, send_from_directory
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

# set path to templates
template_dir = os.getcwd()
template_dir = os.path.join(template_dir, 'templates')

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
UPLOAD_FOLDER = './uploads'

# initialize our Flask application and the Keras model
app = Flask(__name__, template_folder=template_dir)

app.secret_key = "secret key"
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# instantiate model        
model = None

# instantiate the preprocess class
img_preprocess = transforms.Compose([
        transforms.RandomResizedCrop(224),
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])

def _load_model():
    # load the pre-trained Pytorch model
    global model
    model = torch.load('./torch_transfer_resnet_15B_091919.pt', map_location='cpu')

def allowed_file(filename):
    """ function used to ensure file is in expected format"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route("/predict", methods=["POST"])
def predict():
    # initialize the data dictionary that will be returned from the
    # view
    data = {"success": False}

    # ensure an image was properly uploaded to our endpoint
    # Get the file
    if request.method == "POST":
         # check if the post request has the file part
        if 'image' not in request.files:
            flash('No Image')
            return redirect(url_for('index'))
        file = request.files['image']
        file_secure = secure_filename(file.filename)
        # if user does not select file, browser also
        # submit an empty part without filename
        if file_secure == '':
            flash('No selected file')
            return redirect(url_for('index'))
        if not allowed_file(file_secure):
            flash('Wrong File Format!')
            return redirect(url_for('index'))
        if file and allowed_file(file_secure):
            # read the image in PIL format
            image = request.files['image'].read()
            image = Image.open(io.BytesIO(image))
            
            # preprocess the image and prepare it for classification
            image_t = img_preprocess(image)
            batch_t = torch.unsqueeze(image_t,0)
            # classify the input image and then initialize the list
            # of predictions to return to the client
            model.eval()
            out = model(batch_t)
            _, index = torch.max(out,1)
            categories = ['bench press', 'bosu ball', 'elliptical machine',
            'hyper extension bench', 'vibration plate']
            prediction = categories[index[0]]             
            data["success"] = True

    # return the data dictionary as a JSON response
    return redirect(f"https://www.youtube.com/results?search_query={prediction}+tutorial&sp=EgIYAQ%253D%253D") 

if __name__ == "__main__":
    print(("* Loading Pytorch model and Flask starting server..."
        "please wait until server has fully started"))
    _load_model()
    app.run(debug=True)