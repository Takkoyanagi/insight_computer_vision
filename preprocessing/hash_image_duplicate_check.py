import os
from image_hashing import hash_image

direc = "/home/tk/Documents/gym AND battle rope/"
name_list = os.listdir(direc)
name_list.sort()

image_dict = {}

for i in name_list:
    image_dict[i] = hash_image(direc+i)

multi_dict = {}
for key, value in image_dict.items():
    multi_dict.setdefault(value, set()).add(key)

print([values for key, values in multi_dict.items() if len(values) > 1])