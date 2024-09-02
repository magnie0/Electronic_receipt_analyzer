from PIL import Image, ImageOps
import pytesseract
import sys

input = 'End'
def colorChange(filename):
    img = Image.open(filename).convert('RGB')

    r, g, b = img.split()

    img = Image.merge('RGB', (
        r,
        g.point(lambda i: i * 3),  # brighten green channel
        b,
    ))

    img = ImageOps.autocontrast(ImageOps.invert(ImageOps.grayscale(img)), 5)

    img.save(input+filename)

def toText(filename):
    colorChange(filename)
    print(pytesseract.image_to_string(input+filename))
    print(pytesseract.get_languages())

#TODO help if no argument passed
#ex. usage python3 imageToText.py <filename>
filename = sys.argv[1]
toText(filename) 