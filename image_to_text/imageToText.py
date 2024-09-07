from PIL import Image, ImageOps
import pytesseract
import sys

path = './data/'
pathTmp = './data/tmp/'

def colorChange(filename):
    img = Image.open(path+filename).convert('RGB')
    r, g, b = img.split()

    img = Image.merge('RGB', (
        r,
        g.point(lambda i: i * 3),  # brighten green channel
        b,
    ))

    img = ImageOps.autocontrast(ImageOps.invert(ImageOps.grayscale(img)), 5)
    img.save(pathTmp+filename)

def ImagetoText(filename):
    colorChange(filename)
    str = pytesseract.image_to_string(pathTmp+filename)
    return str
