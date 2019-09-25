from image_hashing import hash_image
from PIL import Image
import os

# load the list of categories to download
labels = [labels.rstrip('\n') for labels in open('key_words_updated.txt')]

# create a list of filenames in the directory "image_path"
image_path = []

for label in labels:
    image_path.append("/home/tk/Documents/organized/" + label + "/")


for i in range(len(labels)):
    # name_list[i] = os.listdir("/home/tk/Documents/organized/" + labels[i] + "/")
    name_list = os.listdir("/home/tk/Documents/organized/" + labels[i] + "/")

    # instantiate the dictionary
    image_dict = {}

    # create a dictionary of file name and the hashed value
    for file_nm in name_list:
        image_dict[file_nm] = hash_image(image_path[i]+file_nm)

    # create a reverse dictionary where we count the number of identical hash
    rev_dict = {}
    for key, value in image_dict.items():
        rev_dict.setdefault(value, set()).add(key)

    # isolate duplicated images in the set
    duplicate_set = [values for key, values in rev_dict.items() if len(values) > 1]

    # convert set to list
    duplicate_list = []
    for value in duplicate_set:
        duplicate_list.append(list(value))

    # images to keep in a list
    images_keep = []
    for jpeg in duplicate_list:
        images_keep.append(jpeg[0])

    # create a list of files to delete
    files_to_delete = [x for x in name_list if x not in images_keep]

    # remove duplicated images
    for image in files_to_delete:
        os.remove(image_path[i] + "/" + image)

    print(f"finished with {labels[i]}")
    print(f"{len(labels)} - {i} left to go...")
