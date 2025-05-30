# Script to encode fonts into a framebuffer or something idk

from PIL import Image



def set_arr_len(x, y):
    real_x = x + (x%8) # round to multiple of 8
    return real_x * y #fffffff


def load_image_file(filepath):
    imageh = 0
    imagew = 0
    imgdata = 0
    with Image.open(filepath) as im:
        imgdata = list(im.getdata("R")) #type:ignore
        imageh = im.height
        imagew = im.width
    
    