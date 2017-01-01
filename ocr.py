import pytesseract
import urllib
from PIL import Image
from PIL import ImageFilter
from StringIO import StringIO

def clean(str):
    return str.strip().replace(" ","").replace("\n", "")

def process_image_from_url(url):
    image = Image.open(StringIO(urllib.urlopen(url).read()))
    image.filter(ImageFilter.SHARPEN)
    return pytesseract.image_to_string(image)

def process_image_from_path(path):
    image = Image.open(path)
    image.filter(ImageFilter.SHARPEN)
    return pytesseract.image_to_string(image)

def process_image_from_file(file):
    image = Image.open(file)
    image.filter(ImageFilter.SHARPEN)
    return pytesseract.image_to_string(image)
