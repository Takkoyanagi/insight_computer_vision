# import the necessary packages
from __future__ import print_function, division
import torch
import numpy as np
import io
from torchvision import datasets, models, transforms
from PIL import Image
from flask import render_template, send_from_directory
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from flask_mobility.decorators import mobile_template, mobilized
from flask_app import app

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

# instantiate model        
model = None

def _load_model():
    # load the pre-trained Pytorch model
    global model
    model = torch.load('flask_app/static/torch_transfer_resnet_27CAT__20B_093019.pt', map_location='cpu')

_load_model()

# load the categories
categories = []
with open('flask_app/static/27_category_list.text', 'r') as f:
    for line in f:
        line = line.strip()
        categories.append(line)

# instantiate the preprocess class
img_preprocess = transforms.Compose([
        transforms.RandomResizedCrop(224),
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])

def allowed_file(filename):
    """ function used to ensure file is in expected format"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=['GET', 'POST'])
@mobile_template('{mobile/}index.html')
def index(template):
    return render_template('index.html')

@app.route("/predict", methods=["POST"])
def predict():
    # initialize the data dictionary that will be returned from the
    # view

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
            flash('Wrong File Format! Please use .png, .jpg, or .jpeg')
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
            with torch.no_grad():
                model.eval()
                out = model(batch_t)
                _, index = torch.max(out,1)
                prediction = categories[index[0]]             

    # return the data dictionary as a JSON response
    return redirect(f"https://www.youtube.com/results?search_query={prediction}+tutorial&sp=EgIYAQ%253D%253D")
