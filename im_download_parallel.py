#base code from
#https://stackoverflow.com/questions/56523618/python-download-image-from-url-efficiently
import concurrent.futures
import os
import re

import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs4


def save_image_from_url(idx_row, output_folder='boardgame-pictures'):
    idx,row=idx_row
    page = requests.get(row.image_page)
    soup = bs4(page.content, 'html.parser')
    uncleaned_image_link=(str(soup.find('link',href=re.compile(r'geekdo-images')))) #isolates the full link element to the image
    dl=(re.compile(r'https[^"]*')).findall(uncleaned_image_link) #removes everything except the link iteself
    if dl !=[]:
        dl= dl[0]
        image = requests.get(dl)
        output_path = os.path.join(
            output_folder, row.game_name, row.image_number+dl[-4:]
        )
        print(output_path)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "wb") as f:
            f.write(image.content)
        return dl
    else :
        return uncleaned_image_link

def load(df, output_folder='boardgame-pictures'):    
    with concurrent.futures.ThreadPoolExecutor(max_workers=16) as executor:
        future_to_row = {executor.submit(save_image_from_url, idx_row, output_folder): idx_row  for idx_row in df.iterrows() }
        for future in concurrent.futures.as_completed(future_to_row):
            idx_row = future_to_row[future]
            try:
                dl= future.result()
                idx,row=idx_row
                df.at[idx,'direct_link']=dl
            except Exception as exc:
                print("%r generated an exception: %s" % (idx_row, exc))

df=pd.read_pickle('df_images_tail')
load(df)
pd.to_pickle(df,'df_images_with_direct_links')