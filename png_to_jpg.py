from PIL import Image
import os

def png_to_jpg(image_path):
    if image_path[-3:]=='png':
        print(image_path)
        im = Image.open(image_path)
        os.remove(image_path)
        im.convert('RGB').save(image_path[:-3]+"jpg","JPEG")
    else :
        print('did not touch ' + image_path)
    


directory = 'boardgame-pictures'
#directory='test'
# iterate over files in
# that directory
for root, dirs,files in os.walk(directory):
    for filename in files:
        png_to_jpg(os.path.join(root, filename))