import pandas as pd
from bs4 import BeautifulSoup
import requests   # downloading images
import shutil     # downloading images
import os   
import uuid # generator for file names


data = pd.read_csv("water_tech_image_links.csv")
links = data[data.photo_lnk.notnull()]

### Remove any pre-existing files
os.remove("../data/water_tech_dictionary.csv")
shutil.rmtree('../data/images')
os.mkdir("../data/images")

###  Downloading images
mapping = pd.DataFrame(columns = ["water_tech","fileName"])
maxImages = 1000
for i in range(min(links,maxImages)):
    r = requests.get(links.photo_lnk.iloc[i], stream = True)
    if r.status_code == 200:
        fileName = str(uuid.uuid4()) + ".jpg"
        with open(os.path.join("../data/images/",fileName), 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)
            
            mapping = mapping.append({"water_tech": links.water_tech.iloc[i], "fileName": fileName}, ignore_index = True)

mapping.to_csv("../data/water_tech_dictionary.csv")