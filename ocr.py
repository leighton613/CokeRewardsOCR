import pytesseract
import urllib
from PIL import Image
from PIL import ImageFilter
from StringIO import StringIO
import subprocess as sp
import matlab.engine
from TextDetection import circle2binary


def clean(str):
    return str.strip().replace(" ","").replace("\n", "")
#
# def process_image_from_url(url):
#     image = Image.open(StringIO(urllib.urlopen(url).read()))
#     image.filter(ImageFilter.SHARPEN)
#     return pytesseract.image_to_string(image)
#
# def process_image_from_path(path):
#     return img2str(path)

def process_image_from_file(filename, folder='uploads'):
    circle = rgb2circle(filename, folder)
    binary = circle2img(circle)
    string = ""
    for file in binary:
        string += clean(img2str(file))
    return string



def rgb2circle(filename, folder):
    """
    I step: turn the original rgb to crop a circle.
    :param path: str, filename
    :return: str, new_filename (with '_crop' postfix)
    """
    eng = matlab.engine.start_matlab()
    return eng.circle_crop(folder+'/'+filename)

def circle2img(filename):
    """
    II step: text detection and localization
    :param filename: str (only) filename
    :return: list[str]
    """
    output_list = circle2binary(filename)
    return output_list


def img2str(filename):
    """
    III step: turn text image part into text via OCR API
    :param path: str
    :return: str, recognized text
    """
    cmd = 'tesseract ' + filename + ' stdout -l eng -psm 7 -c tessedit_char_whitelist=0123456789ABCDEFGHIJLMNPQRSTUVWXYZ'
    return sp.check_output(cmd, shell=True)
