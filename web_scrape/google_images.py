# load the necessary modules
from google_images_download import google_images_download #2.8.0
from selenium import webdriver #selenium version 3.141.0
from selenium.common.exceptions import NoSuchAttributeException, WebDriverException

# initialize the chrome driver with selenium
driver = webdriver.Chrome(executable_path='./chromedriver')

# load the list of categories to download
labels = [labels.rstrip('\n') for labels in open('key_words_updated.txt')]
labels

# print the number of categories to download
print(len(labels))

# instantiate the class
response = google_images_download.googleimagesdownload()

# loop over words in the list to start downloads
for i in labels:
    arguments = {"keywords":i,"limit":1000,"print_urls":False, "format":"jpg", "size":"medium", "delay":5, 'chromedriver':"./chromedriver"}
    paths = response.download(arguments)