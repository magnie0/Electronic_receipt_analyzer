from PIL import Image, ImageOps
import pytesseract
import sys

path = './data/'
tmpFile = 'Tmp'
def colorChange(filename):
    img = Image.open(path+filename).convert('RGB')

    r, g, b = img.split()

    img = Image.merge('RGB', (
        r,
        g.point(lambda i: i * 3),  # brighten green channel
        b,
    ))

    img = ImageOps.autocontrast(ImageOps.invert(ImageOps.grayscale(img)), 5)
    #TODO tmp file save somewhere else
    img.save(path+tmpFile+filename)

def ImagetoText(filename):
    colorChange(filename)
    str = pytesseract.image_to_string(path+tmpFile+filename)
    return str
