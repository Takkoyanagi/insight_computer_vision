# import the necessary packages
from __future__ import print_function, division
import torch
# import torch.nn as nn
# import torch.optim as optim
# from torch.optim import lr_scheduler
import numpy as np
import torchvision
import os
import csv
from img_preprocess import process_image

def predict_accuracy(path, v_files=100, filename="predict_1.csv"):
    """loop through expected organized directory, 
    preproccess images,
    categorize and determines accuracy metrics
    then returns a list of [category label, correct prediction,
    unreadable image numbers, number of images in validation set,
    dictionary of misclassified category]
    path = where the validation data is located (i.e. /data/validation/)
    v_files = number of validation files for each
    category
    filename = name you designate for the csv file that gets created"""
    # load trained weights to model and set to evaluation mode
    model = torch.load('./torch_transfer_resnet_25CAT__20B_092819.pt', map_location='cpu')
    model.eval()

    # create a list of image categories and then sort
    labels = os.listdir(path)
    labels.sort()

    # nested for loop to walk from each validation directory ->
    # each categories -> testing image files
    result = []
    for ind, directory in enumerate(os.listdir(path)):
        # instantiate metrics
        correct = 0
        bad_images = 0
        not_list = []      

    # disable gradient calculations to reduce computational need
        with torch.no_grad(): 
            for filename in os.listdir(path+directory):
                try: #in case some jpeg files don't open
                    # process image like training data
                    vec_img = process_image(path+directory+'/'+filename)
                    out = model(vec_img) # predict using trained model
                    _, index = torch.max(out,1) # get the index of prediction
                    # see if we guess correctly
                    if labels[index] == directory:
                        correct += 1
                    #otherwise, store which object detected instead 
                    else:
                        not_list.append({directory:labels[index]})
                except:
                    bad_images += 1 # image files that didn't open
                
        pred = [directory, correct, bad_images, v_files, not_list]
        result.append(pred)
        print(f"finished {int(ind)+int(1)} of {len(os.listdir(path))}")
    return result

path = "/home/tk/Documents/data/validation_set2/"

result = predict_accuracy(path)
with open('result_1', "w") as f:
    writer = csv.writer(f)
    writer.writerows(result)
