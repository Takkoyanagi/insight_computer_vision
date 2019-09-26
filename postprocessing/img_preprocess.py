from PIL import Image
from torchvision import datasets, models, transforms
import torch

def process_image(path):
    """process images before validating the pytorch resnet model
    path = image file path"""
    
    # create an instance for preprocessing
    img_preprocess = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    
    img = Image.open(path) # open image
    img_t = img_preprocess(img) # preprocess image
    vec_img = torch.unsqueeze(img_t,0) # vectorize image
    return vec_img