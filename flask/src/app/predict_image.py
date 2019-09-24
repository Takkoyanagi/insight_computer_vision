from keras.preprocessing import image
from keras.applications.resnet50 import preprocess_input
from keras.models import load_model
import numpy as np
import matplotlib.pyplot as plt

def image_analyzer(img_path, target_size=(299,299)):
    """ takes an image and preprocesses it to feed to the model
        img_path = filepath from the website created using Flask
        target_size = image tuple that was used to train the model
    """ 
    model = load_model('GED_classification_1_ResNet20v1_model.070.h5')
    # img = image.load_img(img_path, target_size=target_size)
    # # plt.imshow(img)
    # # plt.show()
    
    # x = image.img_to_array(img)
    # x = np.expand_dims(x, axis=0)
    # x = preprocess_input(x)
    # preds = model.predict(x, batch_size=1)

    # categories = ['bench press', 'bosu ball', 'elliptical machine', 'hyper extension bench', 'vibration plate']
    # return categories[np.argmax(preds)]
    return 12