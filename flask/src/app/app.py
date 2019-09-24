import os
import urllib
import sys
from flask import render_template, send_from_directory
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
# import predict_image

import tensorflow
from tensorflow.python.keras.preprocessing import image
from tensorflow.python.keras.applications.resnet50 import preprocess_input
from tensorflow.python.keras.models import load_model, model_from_json
import numpy as np




# graph = tf.compat.v1.get_default_graph

model = None

def _load_model():
    # load the pre-trained Keras model (here we are using a model
    # pre-trained on ImageNet and provided by Keras, but you can
    # substitute in your own networks just as easily)
    print("\n\n>>>loading the model.")
    global model
    # model = load_model('GED_classification_1_ResNet20v1_model.070.h5')
    # print(model)
    print("Done loading model")

# with open('model_architecture_299.json', 'r') as f:
#     model = model_from_json(f.read())



# def image_analyzer(img_path, target_size=(299,299)):
#     """ takes an image and preprocesses it to feed to the model
#         img_path = filepath from the website created using Flask
#         target_size = image tuple that was used to train the model
#     """ 
#     # model = load_model('GED_classification_1_ResNet20v1_model.070.h5'
#     print("Model inside function")
#     print(model)
#     img = image.load_img(img_path, target_size=target_size)
#     # plt.imshow(img)
#     # plt.show()
#     print("\n\n\n>>>>>>>>>>>>>>>")
#     # print(model)
#     x = image.img_to_array(img)
#     x = np.expand_dims(x, axis=0)
#     x = preprocess_input(x)
#     preds = model.predict(x, batch_size=1)

#     categories = ['bench press', 'bosu ball', 'elliptical machine', 'hyper extension bench', 'vibration plate']
#     return categories[np.argmax(preds)]
    # return 12

template_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
template_dir = os.path.join(template_dir, 'templates')


app = Flask(__name__, template_folder=template_dir)

app.secret_key = "secret key"
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config.update(dict(
        UPLOAD_FOLDER = "./flib/static/uploads/",
        DISPLAY_FOLDER = "./flib/static/display/",
        TEMP_FOLDER = "./static/uploads/"
        ))

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
@app.route('/uploads')
def upload_file():
    # Get the file
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            global filename
            filename = secure_filename(file.filename)
            global filepath
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            # call your imageAnalyzer function
            # _result = image_analyzer(filepath,(299,299))
            img = image.load_img(filepath, target_size=(299,299))
            print("\n\n\n>>>>>>>>>>>>>>>")
            # print(model)
            x = image.img_to_array(img)
            x = np.expand_dims(x, axis=0)
            x = preprocess_input(x)
            # model = load_model('GED_classification_1_ResNet20v1_model.070.h5')

            print(f"\n\n\n+++++++++++++++++++++++Model is {model}")
            print(f"\n\n\n+++++++++++++++++++++++XXXXXXXX is {x}")
            
            # global graph
            # with graph.as_default():
            #     preds = model.predict(x, batch_size=1)


            categories = ['bench press', 'bosu ball', 'elliptical machine', 'hyper extension bench', 'vibration plate']
            # _result = categories[np.argmax(preds)]
            _result = 'bosu ball'
            return redirect(url_for('result', whatIgotFromAnalysis=_result))

    return render_template("upload_file.html")

@app.route("/analysis")
def result():
    hello = request.args.get('whatIgotFromAnalysis')
    print(f"\n\n\n>>>>>Hello is {hello}")
    return render_template("analysis.html", hello = hello)



@app.route('/about')
def about():
    return render_template("about.html")

# @app.route('/GD')
# def gymDecoder():
#     if request.method == 'POST':
#         return redirect(url_for('home'))
#     return render_template('GD.html')

if __name__ == '__main__':
    print(("* Loading Keras model and Flask starting server..."
        "please wait until server has fully started"))

    _load_model()
    # print("Model before starting the server")
    # print(model)
    app.run(debug=True)