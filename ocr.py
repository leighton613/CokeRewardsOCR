import pytesseract
import urllib
from PIL import Image
from PIL import ImageFilter
from StringIO import StringIO
import subprocess as sp


def clean(str):
    return str.strip().replace(" ","").replace("\n", "")

def process_image_from_url(url):
    image = Image.open(StringIO(urllib.urlopen(url).read()))
    image.filter(ImageFilter.SHARPEN)
    return pytesseract.image_to_string(image)

def process_image_from_path(path):
    return img2str(path)

def process_image_from_file(file):
    image = Image.open(file)
    image.filter(ImageFilter.SHARPEN)
    return pytesseract.image_to_string(image)



def img2str(path):
    cmd = 'tesseract ' + path + ' stdout -l eng -psm 7 -c tessedit_char_whitelist=0123456789ABCDEFGHIJLMNPQRSTUVWXYZ'
    return sp.check_output(cmd, shell=True)
