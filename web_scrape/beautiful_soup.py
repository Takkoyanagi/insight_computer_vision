# load the necessary modules
import requests #version 2.22.10
from bs4 import BeautifulSoup #version 4.7.1
import nltk #version 3.4.4


# get the content/data from the website
urls = ["https://www.gymventures.com/gym-equipment-names-and-pictures/",
        "https://garagegymplanner.com/identifying-various-gym-equipment-with-images/",
       "https://gymperson.com/gym-equipment-names-with-pictures-videos/",
       "https://gymequipmentcenter.com/gym-machine-names/"]

# initialize lists
page = []
soup = []
descriptions_1 = []
descriptions_2 = []

for i, value in enumerate(urls):
    page.append(requests.get(value))
    assert page[i].status_code == 200 # confirm data was scraped correctly

    soup.append(BeautifulSoup(page[i].content, 'html.parser'))

# scrape information from h3 tags
for h3_tags in soup[0].find_all('h3'):
    descriptions_1.append(h3_tags.text)

descriptions_1 = descriptions_1[:26]

# scrape information from a tags
for i in range(1,4):
    for tag in soup[i].find_all('a'):
        if not "":
            descriptions_2.append(tag.text)

# slice and clean list from description_2
desc_1 = descriptions_2[17:63]
desc_1_cleaned = [i.split('\u200b')[0] for i in desc_1]
desc_2 = descriptions_2[209:251]
desc_3 = descriptions_2[480:546]

# concatinate the lists together
all_names = descriptions_1 + desc_1_cleaned + desc_2 + desc_3
all_names = list(set(all_names))

#clean list of words to get rid of similar words using
# NLTK lemmatizer

# instantiate class
lemma = nltk.WordNetLemmatizer()

# lemmatize and lowercase words in list
lemmatized = []
for w in all_names:
    lemmatized.append(lemma.lemmatize(w).lower())

# Remove plural words
deplur = []
for name in lemmatized:
    if name[-1] == 's' and name[-2] != 's':
        deplur.append(name[:-1])
    else:
        deplur.append(name)

deplur = list(set(deplur))
deplur.sort()

# save word list as .txt file
with open('key_words.txt', 'w') as f:
    for item in deplur:
        f.write("%s\n" % item)
