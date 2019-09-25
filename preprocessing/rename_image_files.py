import os
# load the list of categories to download
labels = [labels.rstrip('\n') for labels in open('key_words_updated.txt')]

for i in labels:
    count = 0
    img_dir = "/home/tk/Documents/organized/"+i
    for filename in os.listdir(img_dir):
        os.rename(img_dir + "/" + filename, img_dir + "/" + i + "000000000000000" + str(count) + '.jpeg')
        count += 1