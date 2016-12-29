import pytesseract
import urllib
from PIL import Image
from PIL import ImageFilter
from StringIO import StringIO


def process_image_from_url(url):
    image = Image.open(StringIO(urllib.urlopen(url).read()))
    image.filter(ImageFilter.SHARPEN)
    return pytesseract.image_to_string(image)

def process_image_from_path(path):
    image = Image.open(path)
    return pytesseract.image_to_string(image)
