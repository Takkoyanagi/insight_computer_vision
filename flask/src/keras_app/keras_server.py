# import the necessary packages
from keras.models import load_model
from keras.preprocessing.image import img_to_array
from keras.applications import imagenet_utils
from PIL import Image
import numpy as np
from flask import Flask, render_template, request, url_for, jsonify
import io
import os

# set path to templates
template_dir = os.getcwd()
template_dir = os.path.join(template_dir, 'templates')

# initialize our Flask application and the Keras model
app = Flask(__name__, template_folder=template_dir)
model = None

def _load_model():
    # load the pre-trained Keras model (here we are using a model
    # pre-trained on ImageNet and provided by Keras, but you can
    # substitute in your own networks just as easily)
    
    global model
    # model = load_model('GED_classif_2_R224_S5_B10_ResNet29v2_model.072.h5')
    model = load_model('GED_classification_1_ResNet20v1_model.070.h5')
    
    print(model)

def prepare_image(image, target):
    # if the image mode is not RGB, convert it
    if image.mode != "RGB":
        image = image.convert("RGB")

    # resize the input image and preprocess it
    image = image.resize(target)
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)
    image = imagenet_utils.preprocess_input(image)

    # return the processed image
    return image

@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route("/predict", methods=["POST"])
def predict():
    # initialize the data dictionary that will be returned from the
    # view
    data = {"success": False}

    # ensure an image was properly uploaded to our endpoint
    if request.method == "POST":
        if request.files.get("image"):
            # read the image in PIL format
            image = request.files["image"].read()
            image = Image.open(io.BytesIO(image))

            # preprocess the image and prepare it for classification
            image = prepare_image(image, target=(299, 299))

            # classify the input image and then initialize the list
            # of predictions to return to the client
           
            preds = model.predict(image)
            # preds = [0,1,0,0,0]
            # results = imagenet_utils.decode_predictions(preds)
            
            categories = ['bench press', 'bosu ball', 'elliptical machine',
            'hyper extension bench', 'vibration plate']
            result = categories[np.argmax(preds)]
            data['prediction'] = result
            # # loop over the results and add them to the list of
            # # returned predictions
            # for (imagenetID, label, prob) in results[0]:
            #     r = {"label": label, "probability": float(prob)}
            #     data["predictions"].append(r)

            # indicate that the request was a success
            data["success"] = True

    # return the data dictionary as a JSON response
    return jsonify(data)
    # if this is the main thread of execution first load the model and
# then start the server
if __name__ == "__main__":
    print(("* Loading Keras model and Flask starting server..."
        "please wait until server has fully started"))
    _load_model()
    app.run(debug=False)