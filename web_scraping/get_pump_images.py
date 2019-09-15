import pandas as pd
import requests   # downloading images
import shutil     # downloading images
import os   
import uuid # generator for file names
import numpy as np


data = pd.read_csv("water_tech_image_links_cleaned.csv")
links = data[data.photo_lnk.notnull()]
links.loc[:, 'clean_water_tech'] = links.clean_water_tech.str.strip()

### Remove any pre-existing files
shutil.rmtree('../data/images')
os.mkdir("../data/images")

num_pics_per_class = 100

classes = links.clean_water_tech.unique()
classes = np.delete(classes, np.where((classes == 'NO_MAPPING') |
                                      (pd.isnull(classes))))

###  Downloading images
for x in links.clean_water_tech.unique():
    
    links_class = links[links.clean_water_tech == x]
    tries = 0
    success = 0
    
    while ((success < num_pics_per_class) & (len(links_class.index) > tries)):

        r = requests.get(links_class.photo_lnk.iloc[tries], stream = True)
        tries += 1
        
        if ((r.status_code == 200) and (len(r.content) > 30000)):

            success += 1
            fileName = str(uuid.uuid4()) + ".jpg"
            
            # make sub-directory for class if not present
            os.makedirs(os.path.join("../data/images", x), exist_ok=True)
            
            # save image to sub-directory
            with open(os.path.join("../data/images", x, fileName),
                      'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)
                