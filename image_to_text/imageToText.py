from PIL import Image, ImageOps
import pytesseract
import cv2
import numpy as np

path = './data/'
pathTmp = './data/tmp/' #path for tmp files

#from yt video
#https://www.youtube.com/watch?v=ADV-AjAXHdc&t=305s

#1. invert image
def invert(img):
    return cv2.bitwise_not(img)
    

#3.1 
def grayscale(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#4 Noise removal
def noise_removal(img):
    kernel = np.ones((1,1), np.uint8)
    img = cv2.dilate(img, kernel, iterations=1)
    kernel = np.ones((1,1), np.uint8)
    img = cv2.erode(img, kernel, iterations=1) #thining pixels down
    # img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
    # img = cv2.medianBlur(img, 3)
    return img

def example_processing(filename):
    #Open image
    img = cv2.imread(path+filename)

    #1.invert exact opposite
    inv = invert(img)
    cv2.imwrite(pathTmp+"inv"+filename, inv)

    #2. rescaling: optimal range for height of characters (DPI)

    #3. Binarization: convert an image to black and white, first it has to be in grayscale
    #3.1
    gray_image = grayscale(img)
    cv2.imwrite(pathTmp+"gray"+filename, gray_image)
    #3.2 threshold
    thresh, im_bw = cv2.threshold(gray_image, 127, 255, cv2.THRESH_BINARY)
    cv2.imwrite(pathTmp+"b_and_w"+filename, im_bw)

    #4 Noise removal
    no_noise = noise_removal(im_bw)
    cv2.imwrite(pathTmp+"no_noise"+filename, no_noise)

    #5 Dilation and erosion, when no noise around letters but some different thin

def ImagetoText(filename):

    img = cv2.imread(path+filename)
    img = grayscale(img)
    cv2.imwrite(pathTmp+"1"+filename, img)
    ithresh, img = cv2.threshold(img, 23, 255, cv2.THRESH_TOZERO)
    cv2.imwrite(pathTmp+"2"+filename, img)
    img = invert(img)
    cv2.imwrite(pathTmp+"3"+filename, img)
    img = noise_removal(img)
    cv2.imwrite(pathTmp+"4"+filename, img)
  
    data = pytesseract.image_to_string(img, lang='eng', config='--psm 6')
    return data

